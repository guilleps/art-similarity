import os
import uuid
import json
import logging

from transformations.infrastructure.exceptions import EmbeddingModelError
from transformations.domain.models import TransformedImageEmbedding
from .cloudinary_service import CloudStorageService
from .embedding_extractor import VGG19EmbeddingExtractor
from .external_request_service import ExternalRequestService

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.embedding_extractor = VGG19EmbeddingExtractor()
        self.cloudinary_service = CloudStorageService()
        self.external_service = ExternalRequestService()

    def process_and_save_embeddings(self, session, transformed_data: dict) -> dict:
        lookup = {1: {}, 2: {}}

        for index, key in enumerate(["image_1", "image_2"], start=1):
            for transform_type, image_url in transformed_data[key].items():
                if transform_type == "original_image":
                    continue

                try:

                    image_bytes = self.external_service.fetch_bytes(image_url)

                    os.makedirs("/tmp", exist_ok=True)
                    temp_image_path = "/tmp/uploaded_image.jpg"

                    try:
                        with open(temp_image_path, "wb") as f:
                            f.write(image_bytes)

                        # Generar embedding
                        embedding = self.embedding_extractor.extract_embedding(
                            temp_image_path
                        )

                        # Guardar embedding en JSON
                        embedding_id = str(uuid.uuid4())
                        json_path = f"/tmp/embedding_{embedding_id}.json"

                        with open(json_path, "w") as f:
                            json.dump(embedding, f)

                        secure_url = self.cloudinary_service.upload_file_to_cloudinary(
                            json_path, f"embedding_{embedding_id}.json"
                        )
                        logger.info("Embedding subido a Cloudinary: %s", secure_url)

                        embedding_url = secure_url

                    finally:
                        if os.path.exists(temp_image_path):
                            os.remove(temp_image_path)
                        if os.path.exists(json_path):
                            os.remove(json_path)

                except Exception as e:
                    logger.error(
                        f"[EMBEDDING ERROR] transform_type={transform_type} | url={image_url} | error={str(e)}",
                        exc_info=True,
                    )
                    raise EmbeddingModelError("Error al generar el embedding") from e

                TransformedImageEmbedding.objects.create(
                    comparison=session,
                    image_index=index,
                    transform_type=transform_type,
                    image_url=image_url,
                    embedding_url=embedding_url,
                )

                # Store for similarity lookup
                lookup[index][transform_type] = embedding_url

        return lookup
