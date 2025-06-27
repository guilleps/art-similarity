import logging
from sklearn.metrics.pairwise import cosine_similarity
from api.domain.models import SimilarityMetricResult
from api.infrastructure.services.external_request_service import ExternalRequestService

logger = logging.getLogger(__name__)

class SimilarityService:

    def compute_and_save(self, session, embeddings: dict):
        for transform in embeddings[1].keys() & embeddings[2].keys():
            url_1 = embeddings[1].get(transform)
            url_2 = embeddings[2].get(transform)

            if not url_1 or not url_2:
                logger.warning(f"[SIMILARITY] Skipping {transform} due to missing URLs: file_1={url_1}, file_2={url_2}")
                continue

            emb_1 = ExternalRequestService.fetch_json(url_1)
            emb_2 = ExternalRequestService.fetch_json(url_2)

            similarity = cosine_similarity([emb_1], [emb_2])[0][0]
            
            SimilarityMetricResult.objects.create(
                comparison=session,
                transform_type=transform,
                similarity_score=similarity,
                file_1=url_1,
                file_2=url_2
            )
