import os
import requests

TRANSFORM_SERVICE_URL = os.environ.get("TRANSFORM_SERVICE_URL")

class TransformationService:
    def transform_images(self, image_1_url: str, image_2_url: str) -> dict:
        response = requests.post(f"{TRANSFORM_SERVICE_URL}/transform", json={
            "image_1_url": image_1_url,
            "image_2_url": image_2_url
            })
        response.raise_for_status()
        return response.json()
    