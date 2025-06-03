import tensorflow as tf
import numpy as np
import json
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
from tensorflow.keras.models import Model
import io

import os
# no mostrar logs de info
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tf.config.threading.set_intra_op_parallelism_threads(4)
tf.config.threading.set_inter_op_parallelism_threads(2)

def load_efficientnet_model():
    base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
    base_model.trainable = False
    model = Model(inputs=base_model.input, outputs=base_model.output)
    return model

efficientnet_model = load_efficientnet_model()

def generate_embedding(img_bytes, output_path=None):
    img = image.load_img(io.BytesIO(img_bytes), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    embedding = efficientnet_model.predict(img_array)

    if output_path:
        np.save(output_path, embedding)
        with open(output_path, 'w') as json_file:
            json.dump(embedding.flatten().tolist(), json_file)
        
    return embedding.flatten().tolist() 

image_path = './soir_bleu.jpg'
output_path = f'./soir_bleu_embedding.json'

with open(image_path, 'rb') as f:
    img_bytes = f.read()

generate_embedding(img_bytes, output_path)