import tensorflow as tf
import keras
from keras.applications import EfficientNetB2

IMG_SIZE = 256
BATCH_SIZE = 64

model = EfficientNetB2(
    include_top=False, 
    weights='imagenet',
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

print("Backend actual:", keras.backend.backend())
print("Número de capas EfficientNetB2:", len(model.layers))