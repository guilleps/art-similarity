import tensorflow as tf
from tensorflow.keras import models, callbacks
from tensorflow.keras.utils import image_dataset_from_directory
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np

BATCH_SIZE = 32
IMG_SIZE = (256, 256)

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

    return train_ds.prefetch(tf.data.AUTOTUNE), test_ds.prefetch(tf.data.AUTOTUNE)

# CALLBACKS
def get_callbacks(phase):
    return [
        callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        callbacks.ModelCheckpoint(f"efficientnet_phase{phase}.keras", save_best_only=True),
        callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
    ]

def evaluate_embeddings(model, dataset):
    feature_model = models.Model(inputs=model.input, outputs=model.get_layer("embedding").output)
    embeddings = []
    labels = []

    for batch in dataset:
        imgs, lbls = batch
        emb = feature_model.predict(imgs)
        embeddings.append(emb)
        labels.extend(lbls.numpy())

    embeddings = np.concatenate(embeddings)
    labels = np.array(labels)

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

def resume_phase3():
    train_ds, test_ds = load_datasets()

    # Cargar el modelo guardado al cortar la Fase 3
    print("🔁 Cargando modelo guardado: efficientnet_phase3.keras...")
    model = tf.keras.models.load_model("efficientnet_phase3.keras")

    # Asegurar que todas las capas estén entrenables
    model.trainable = True
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    print("✅ Reanudando Fase 3...")
    model.fit(train_ds, validation_data=test_ds, epochs=6, callbacks=get_callbacks(3))  # puedes ajustar epochs

    evaluate_embeddings(model, test_ds)

if __name__ == "__main__":
    resume_phase3()
