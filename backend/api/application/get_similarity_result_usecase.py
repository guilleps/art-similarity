from api.domain.models import ImageComparisonSession, TransformedImageEmbedding, SimilarityMetricResult
from django.core.exceptions import ObjectDoesNotExist

class GetSimilarityResultUseCase:
    def execute(self, comparison_id):
        try:
            session = ImageComparisonSession.objects.get(id=comparison_id)
        except ObjectDoesNotExist:
            raise ValueError(f"No se encontró la sesión de comparación con ID: {comparison_id}")

        embeddings = TransformedImageEmbedding.objects.filter(comparison=session)
        image_dict = {1: {}, 2: {}}

        # 1. Agrupar transformaciones por imagen
        for emb in embeddings:
            if emb.transform_type == "original_image":
                image_dict[emb.image_index]["original_image"] = emb.embedding_url
            else:
                image_dict[emb.image_index][emb.transform_type] = {
                    "image_transformed": emb.image_url,
                    # "embedding": emb.embedding_url
                }

        # 2. Agrupar similitudes
        similarities = SimilarityMetricResult.objects.filter(comparison=session)
        similarity_block = {}

        for sim in similarities:
            emb1 = TransformedImageEmbedding.objects.filter(
                comparison=session, embedding_url=sim.file_1
            ).first()
            emb2 = TransformedImageEmbedding.objects.filter(
                comparison=session, embedding_url=sim.file_2
            ).first()

            similarity_block[sim.transform_type] = {
                "files": [
                    emb1.image_url if emb1 else "",
                    emb2.image_url if emb2 else ""
                ],
                "similarity": round(sim.similarity_score, 4)
            }

        return {
            "comparison_id": str(comparison_id),
            "imagen_1": image_dict[1],
            "imagen_2": image_dict[2],
            "similitud": similarity_block
        }
