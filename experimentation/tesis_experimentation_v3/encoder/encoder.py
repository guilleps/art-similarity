import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.applications.efficientnet import preprocess_input
import numpy as np
from PIL import Image

# construimos el embudo a reduccion de 10 - 15 dimensiones
def encoder_built(
        output_dim=15, 
        input_shape=(256, 256, 3) # input esperado a 3 canales (RGB) y tamaño 256x256
        ):
    base_model = EfficientNetB2(include_top=False, weights='imagenet', input_shape=input_shape) # suele esperar 260x260
    base_model.trainable = False  # descartamos el modelo base de clasificacion

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dense(128, activation='relu'),
        Dense(output_dim, activation=None)  # salida a 15 dimensiones
    ])
    return model

# encoder = encoder_built()
# encoder.summary()

# procesamiento de imagen
def load_process_image(path, target_size=(256, 256)):
    img = Image.open(path).convert('RGB')
    img = img.resize(target_size)
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)  # conversion a un lote (1=batch, 256=dim_h, 256=dim_w, 3=channel)