import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import EfficientNetB0, EfficientNetB2
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.utils import image_dataset_from_directory
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np
import wandb
from wandb.keras import WandbCallback

wandb.init(project="art_similarity_ft_test")
config = wandb.config

# CONFIG GLOBAL
BATCH_SIZE = 32
IMG_SIZE = (256, 256)
EPOCHS_PHASE1 = 5
EPOCHS_PHASE2 = 5
EPOCHS_PHASE3 = 5

# ARCHITECTURE SELECTION
if config.architecture == "EfficientNetB0":
    BaseNet = EfficientNetB0
elif config.architecture == "EfficientNetB2":
    BaseNet = EfficientNetB2
else:
    raise ValueError("Invalid architecture selected.")

# DATA LOADING
def load_datasets():
    train_ds = image_dataset_from_directory(
        "C:/workspace/data/train_sampled",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='int',
        shuffle=True
    )
    test_ds = image_dataset_from_directory(
        "C:/workspace/data/test",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='int',
        shuffle=False
    )
    return train_ds.prefetch(tf.data.AUTOTUNE), test_ds.prefetch(tf.data.AUTOTUNE)

# AUGMENTATION
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.1, 0.1),
    layers.Lambda(preprocess_input)
])

# MODEL CREATION
def build_model(trainable_layers=None):
    base_model = BaseNet(include_top=False, weights='imagenet', input_shape=(*IMG_SIZE, 3))
    base_model.trainable = trainable_layers is not None
    if trainable_layers:
        for layer in base_model.layers[:-trainable_layers]:
            layer.trainable = False
    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = data_augmentation(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    embeddings = layers.Dense(config.embedding_dim, activation=None, name="embedding")(x)
    outputs = layers.Dense(10, activation='softmax')(embeddings)
    return models.Model(inputs, outputs)

# SCHEDULE LR
def slanted_triangular_lr(max_lr, total_epochs):
    def scheduler(epoch):
        pct = epoch / total_epochs
        if pct < 0.3:
            return max_lr * (pct / 0.3)
        else:
            return max_lr * (1 - (pct - 0.3) / 0.7)
    return scheduler

# EVALUACIÓN EMBEDDINGS
def evaluate_embeddings(model, dataset):
    feature_model = models.Model(inputs=model.input, outputs=model.get_layer("embedding").output)
    embeddings = feature_model.predict(dataset, verbose=0)
    labels = np.concatenate([y.numpy() for _, y in dataset])
    sil_score = silhouette_score(embeddings, labels)
    nn = NearestNeighbors(n_neighbors=6, metric='cosine').fit(embeddings)
    _, indices = nn.kneighbors(embeddings)
    correct = sum(np.sum(labels[neighbors[1:]] == labels[i]) for i, neighbors in enumerate(indices))
    p_at_5 = correct / (len(labels) * 5)
    wandb.log({"silhouette_score": sil_score, "precision_at_5": p_at_5})

wandb.log({
    "silhouette_score": sil_score,
    "precision_at_5": precision_at_5
})

# ENTRENAMIENTO
train_ds, test_ds = load_datasets()

# Phase 1
model = build_model(trainable_layers=None)
model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE1, callbacks=[WandbCallback()])
evaluate_embeddings(model, test_ds)

# Phase 2
model = build_model(trainable_layers=config.trainable_layers)
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
lr_schedule = callbacks.LearningRateScheduler(slanted_triangular_lr(config.learning_rate_phase2, EPOCHS_PHASE2))
model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE2, callbacks=[WandbCallback(), lr_schedule])
evaluate_embeddings(model, test_ds)

# Phase 3
model = build_model(trainable_layers=len(BaseNet(weights='imagenet', include_top=False).layers))
model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE3, callbacks=[WandbCallback()])
evaluate_embeddings(model, test_ds)

wandb.finish()
