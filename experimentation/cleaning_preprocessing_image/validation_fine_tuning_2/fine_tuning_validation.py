import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import EfficientNetB2
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.utils import image_dataset_from_directory
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
import sys
import datetime
from datetime import datetime

tf.config.threading.set_intra_op_parallelism_threads(4)
tf.config.threading.set_inter_op_parallelism_threads(2)

# CONFIGURACIÓN GENERAL
BATCH_SIZE = 32

# interpolacion, simplifica input pero puedes perder fine-grained style information
IMG_SIZE = (256, 256) # 256 por pruebas
EPOCHS_PHASE1 = 5
EPOCHS_PHASE2 = 5
EPOCHS_PHASE3 = 5
EMBEDDING_DIM = 256

# DATASET LOADING
def load_datasets():
    train_ds = image_dataset_from_directory(
        "C:/workspace/data/train_sampled", # 5000 imagenes
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

# AUGMENTACIÓN
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(height_factor=0.1, width_factor=0.1),
    layers.Lambda(preprocess_input)
], name="data_augmentation")

# MODELO BASE
def build_model(trainable_layers=None):
    base_model = EfficientNetB2(include_top=False, weights='imagenet', input_shape=(*IMG_SIZE, 3))
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
    embeddings = layers.Dense(EMBEDDING_DIM, activation=None, name="embedding")(x)
    outputs = layers.Dense(10, activation='softmax')(embeddings)

    model = models.Model(inputs, outputs)
    model.summary()
    return model

# CALLBACKS
def get_callbacks(phase, model=None, dataset=None):
    base_callbacks =  [
        callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        callbacks.ModelCheckpoint(f"efficientnet_phase{phase}.keras", save_best_only=True),
        callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
    ]

    if model and dataset:
        eval_callback = callbacks.LambdaCallback(
            on_epoch_end=lambda epoch, logs: evaluate_embeddings(model, dataset, silent=True)
        )
        base_callbacks.append(eval_callback)

    return base_callbacks

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
    model = build_model(trainable_layers=None)
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE1, callbacks=get_callbacks(1, model, test_ds), verbose=1)

    # FASE 2: Gradual Unfreezing desde block6 (estimado: x últimas capas)
    model = build_model(trainable_layers=25)
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    lr_scheduler = callbacks.LearningRateScheduler(slanted_triangular_lr(1e-4, EPOCHS_PHASE2))
    model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE2, callbacks=[lr_scheduler] + get_callbacks(2, model, test_ds), verbose=1)

    # FASE 3: Full Fine-Tuning
    model = build_model(trainable_layers=len(EfficientNetB2(weights='imagenet', include_top=False).layers))
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(train_ds, validation_data=test_ds, epochs=EPOCHS_PHASE3, callbacks=get_callbacks(3, model, test_ds), verbose=1)

    return model, test_ds

# EVALUACIÓN EMBEDDINGS
def evaluate_embeddings(model, dataset, silent=False):
    try:
        feature_model = models.Model(inputs=model.input, outputs=model.get_layer("embedding").output)
        embeddings = feature_model.predict(dataset, verbose=0)
        labels = np.concatenate([y.numpy() for _, y in dataset])

        sil_score = silhouette_score(embeddings, labels)
        precision_at_5 = 0
        nn = NearestNeighbors(n_neighbors=6, metric='cosine').fit(embeddings)
        distances, indices = nn.kneighbors(embeddings)

        correct = 0
        for i, neighbors in enumerate(indices):
            true_label = labels[i]
            retrieved_labels = labels[neighbors[1:]]
            correct += np.sum(retrieved_labels == true_label)
        precision_at_5 = correct / (len(labels) * 5)

        if not silent:
            print(f"[Eval] Silhouette Score: {sil_score:.4f} | Precision@5: {precision_at_5:.4f}")
        else:
            print(f"[Epoch Eval] Silhouette={sil_score:.4f}, P@5={precision_at_5:.4f}")

    except Exception as e:
        print(f"[Eval] Error: {str(e)}")

if __name__ == "__main__":
    with open("training_log.txt", "w") as f:
        sys.stdout = f
        sys.stderr = f

        f.write(f"# Fine-Tuning Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        model, test_dataset = train_model()
        evaluate_embeddings(model, test_dataset)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        print('Fin de la tuneaita, guardadinho en .txt')
