import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import EfficientNetB2
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.utils import image_dataset_from_directory
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np

tf.config.threading.set_intra_op_parallelism_threads(4)
tf.config.threading.set_inter_op_parallelism_threads(2)

# CONFIGURACIÓN GENERAL
BATCH_SIZE = 32
IMG_SIZE = (260, 260) # interpolacion, simplifica input pero puedes perder fine-grained style information
EPOCHS_PHASE1 = 10
EPOCHS_PHASE2 = 10
EPOCHS_PHASE3 = 10
EMBEDDING_DIM = 128

# DATASET LOADING
def load_datasets():
    train_ds = image_dataset_from_directory(
        "C:/workspace/data/train",
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

    train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y)).prefetch(tf.data.AUTOTUNE)
    test_ds = test_ds.map(lambda x, y: (preprocess_input(x), y)).prefetch(tf.data.AUTOTUNE)
    return train_ds, test_ds

# AUGMENTACIÓN SOLO PARA ENTRENAMIENTO
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(height_factor=0.1, width_factor=0.1),
], name="data_augmentation")

# MODELO BASE
def build_model(base_model):
    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = data_augmentation(inputs)
    x = base_model(x, training=True)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    embeddings = layers.Dense(EMBEDDING_DIM, activation=None, name="embedding")(x)
    outputs = layers.Dense(10, activation='softmax')(embeddings)
    return models.Model(inputs, outputs)

# CALLBACKS
def get_callbacks(phase):
    return [
        callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        callbacks.ModelCheckpoint(f"efficientnet_phase{phase}.keras", save_best_only=True),
        callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
    ]

# SCHEDULE DE LEARNING RATE TRIANGULAR
def slanted_triangular_lr(max_lr, total_epochs):
    def scheduler(epoch):
        pct = epoch / total_epochs
        if pct < 0.3:
            return max_lr * (pct / 0.3)
        else:
            return max_lr * (1 - (pct - 0.3) / 0.7)
    return scheduler

# ENTRENAMIENTO
def train_model():
    train_ds, test_ds = load_datasets()

    # FASE 1: Feature Extraction
    base_model = EfficientNetB2(include_top=False, weights='imagenet', input_shape=(*IMG_SIZE, 3))
    base_model.trainable = False
    model = build_model(base_model)
    model.summary()
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE1, callbacks=get_callbacks(1), verbose=1)

    # FASE 2: Gradual Unfreezing desde block6 (estimado: 50 últimas capas)
    for layer in base_model.layers[-50:]:
        layer.trainable = True
    model.summary()
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    lr_scheduler = callbacks.LearningRateScheduler(slanted_triangular_lr(1e-4, EPOCHS_PHASE2))
    model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE2, callbacks=[lr_scheduler] + get_callbacks(2), verbose=1)

    # FASE 3: Full Fine-Tuning
    # activamos TODO el modelo base (esto sobrescribe el gradual unfreezing de la fase 2)
    base_model.trainable = True
    model.summary()
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE3, callbacks=get_callbacks(3), verbose=1)

    return model, test_ds

# EVALUACIÓN EMBEDDINGS
def evaluate_embeddings(model, dataset):
    try:
        feature_model = models.Model(inputs=model.input, outputs=model.get_layer("embedding").output)
        embeddings = []
        labels = []
        for batch in dataset:
            imgs, lbls = batch
            emb = feature_model(imgs, training=False)
            embeddings.append(emb.numpy())
            labels.append(lbls.numpy())

        embeddings = np.concatenate(embeddings)
        labels = np.concatenate(labels)

        # Silhouette
        sil_score = silhouette_score(embeddings, labels)
        print(f"Silhouette Score: {sil_score:.4f}")

        # Precision@5
        nn = NearestNeighbors(n_neighbors=6, metric='cosine').fit(embeddings)
        distances, indices = nn.kneighbors(embeddings)

        correct = 0
        for i, neighbors in enumerate(indices):
            true_label = labels[i]
            retrieved_labels = labels[neighbors[1:]]
            correct += np.sum(retrieved_labels == true_label)

        precision_at_5 = correct / (len(labels) * 5)
        print(f"Precision@5: {precision_at_5:.4f}")
    except Exception as e:
        print(f"Error durante la evaluación de embeddings: {str(e)}")

if __name__ == "__main__":
    model, test_dataset = train_model()
    evaluate_embeddings(model, test_dataset)
