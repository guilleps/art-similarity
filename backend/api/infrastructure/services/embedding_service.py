import os
import logging

from api.infrastructure.exceptions import EmbeddingModelError
from api.domain.models import TransformedImageEmbedding
from api.infrastructure.services.external_request_service import ExternalRequestService

logger = logging.getLogger(__name__)

CNN_URL = os.environ.get("CNN_URL")

class EmbeddingService:
    def __init__(self):
        self.external_service = ExternalRequestService()

    def process_and_save_embeddings(self, session, transformed_data: dict) -> dict:
        lookup = {1: {}, 2: {}}
        for index, key in enumerate(["imagen_1", "imagen_2"], start=1):
            for transform_type, image_url in transformed_data[key].items():
                if transform_type == "original_image":
                    continue

                try:
                    image_bytes = self.external_service.fetch_bytes(image_url)
                    embedding_data = self.external_service.post_image_and_get_json(
                        f"{CNN_URL}/embed", image_bytes, headers={"Content-Type": "image/jpeg"}
                    )
                    embedding_url = embedding_data["embedding_url"]
                except Exception as e:
                    logger.error(f"[EMBEDDING ERROR] transform_type={transform_type} | url={image_url} | error={str(e)}", exc_info=True)
                    raise EmbeddingModelError("Fallo al generar embedding desde el microservicio CNN") from e
                
                # Save the transformed image embedding
                TransformedImageEmbedding.objects.create(
                    comparison=session,
                    image_index=index,
                    transform_type=transform_type,
                    image_url=image_url,
                    embedding_url=embedding_url
                )

                # Store for similarity lookup
                lookup[index][transform_type] = embedding_url
        return lookup
    