import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.layers import Input, Lambda
from tensorflow.keras.models import Model

# Definir modelo funcional
input_tensor = Input(shape=(224, 224, 3), name="input_image")
x = Lambda(preprocess_input)(input_tensor)
base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
embedding_output = base_model(x)

model = Model(inputs=input_tensor, outputs=embedding_output, name="efficientnet_embedding")

# Warmup
_ = model(tf.zeros((1, 224, 224, 3), dtype=tf.float32))

# Guardar en formato SavedModel directamente con .save()
model.export("model/1")