import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras import layers, models
from tensorflow.keras.utils import load_img, img_to_array

batch_size = 32
img_size = (224, 224)

image_path = './soir_bleu.jpg'
output_path = './soir_bleu_embedding.npy'

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "C:/workspace/data/train",
    image_size = img_size,
    batch_size = batch_size,
    label_mode = 'categorical'
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "C:/workspace/data/test",
    image_size=img_size,
    batch_size = batch_size,
    label_mode = 'categorical'
)

class_names = train_ds.class_names
num_classes = len(class_names)
print(f"Clases actuales: {class_names}")

AUTOTUNE = tf.data.AUTOTUNE
def preprocess(image, label):
    return preprocess_input(image), label

train_ds = train_ds.map(preprocess, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
val_ds = val_ds.map(preprocess, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)

base_model = EfficientNetB0(
    include_top=False, 
    weights='imagenet', 
    input_shape=(224, 224, 3))
# detenemos el entrenamiento
# extractor de características, sin modificar su conocimiento original
base_model.trainable = False 

inputs = tf.keras.Input(shape=(224, 224, 3))
x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = tf.keras.Model(inputs, outputs)

model.summary()

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# entrenamiento del modelo
history = model.fit(train_ds, validation_data = val_ds, epochs = 5)

# tuneito
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

init_epoch = 5
fine_tune_epochs = 10
total_epochs = init_epoch + fine_tune_epochs

history_fine_tune = model.fit(
    train_ds, 
    validation_data = val_ds, 
    initial_epoch = init_epoch,
    epochs = total_epochs
)

# extraccion de embedding con modelo mejorado

embedding_model = Model(
    inputs=model.input, 
    outputs=model.layers[-3].output # desde la capa (densa)
)

img = load_img(image_path, target_size=img_size)
img_array = img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

embedding = embedding_model.predict(img_array)

np.save(output_path, embedding)
print(f"guardadito")
