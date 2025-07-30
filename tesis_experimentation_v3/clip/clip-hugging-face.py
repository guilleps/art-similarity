import torch
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO

url = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRLM_YMOn41npXKC5fX-TSRfe20jO-nK1cfON36eskj5100UzlH4JMmJVsjNYxZPV4R0vw6DHIw0dqN-osUB5Iw7Q"
image = Image.open(BytesIO(requests.get(url).content))

clip = pipeline(
   task="zero-shot-image-classification",
   model="openai/clip-vit-base-patch32",
   device=0 if torch.cuda.is_available() else -1
)

labels = ["a photo of a cat", "a photo of a dog", "a photo of a car"]

result = clip(image, candidate_labels=labels)
print(result)