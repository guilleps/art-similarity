import uuid
import base64
import random

PINECONE_DIMENSION = 156

def generate_id_for_image():
    return str(uuid.uuid4())

def generate_embbeding(img_bytes):
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    random.seed(len(img_base64))
    return [random.random() for _ in range(PINECONE_DIMENSION)]
