import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
from tensorflow.keras.models import Model
import io

from api.infrastructure.exceptions import EmbeddingModelError

_efficient_model = None

def load_efficientnet_model():
    base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
    model = Model(inputs=base_model.input, outputs=base_model.output)
    return model

# efficientnet_model = 

def generate_embbeding(img_bytes):
    global _efficient_model

    try:

        if _efficient_model is None:
            _efficient_model = load_efficientnet_model()

        img = image.load_img(io.BytesIO(img_bytes), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        embedding = _efficient_model.predict(img_array)
        return embedding.flatten().tolist()
    except Exception as e:
        raise EmbeddingModelError() from e