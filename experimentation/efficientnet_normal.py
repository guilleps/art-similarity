import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
from tensorflow.keras.models import Model
import io

image_path = './soir_bleu.py'

def load_efficientnet_model():
    base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
    model = Model(inputs=base_model.input, outputs=base_model.output)
    return model

efficientnet_model = load_efficientnet_model()

def generate_embedding(img_bytes):
    img = image.load_img(io.BytesIO(img_bytes), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    embedding = efficientnet_model.predict(img_array)
    return embedding.flatten().tolist() 

image_path = './soir_bleu.jpg'
output_path = f'./soir_bleu_embedding_basic.npy'

with open(image_path, 'rb') as f:
    img_bytes = f.read()

generate_embedding(img_bytes, output_path)