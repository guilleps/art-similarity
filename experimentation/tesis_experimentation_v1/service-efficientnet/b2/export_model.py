import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.layers import Input
import numpy as np

# Cargar el modelo entrenado con custom_objects
trained_model = load_model(
    "efficientnet_phase3_b2.keras", 
    compile=False,
    custom_objects={"preprocess_input": preprocess_input}
)

# Reconstruir modelo limpio (sin Lambda ni data_augmentation)
input_tensor = Input(shape=(256, 256, 3), name="input_image")
x = trained_model.get_layer("efficientnetb2")(input_tensor)
x = trained_model.get_layer("global_average_pooling2d_2")(x)
x = trained_model.get_layer("batch_normalization_2")(x)
x = trained_model.get_layer("dropout_2")(x)
output = trained_model.get_layer("embedding")(x)

embedding_model = Model(inputs=input_tensor, outputs=output)

# Warmup
_ = embedding_model(tf.zeros((1, 256, 256, 3)))

# Exportar como SavedModel
embedding_model.export("model/1")
