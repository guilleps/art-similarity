from api.domain.models import ImageComparisonSession, TransformedImageEmbedding, SimilarityMetricResult
from django.core.exceptions import ObjectDoesNotExist

class GetSimilarityResultUseCase:
    def execute(self, comparison_id):
        try:
            session = ImageComparisonSession.objects.get(id=comparison_id)
        except ObjectDoesNotExist:
            raise ValueError(f"No se encontró la sesión de comparación con ID: {comparison_id}")

        # Embeddings: Agrupar por image_index y transform_type
        embeddings = TransformedImageEmbedding.objects.filter(comparison=session)
        image_dict = {1: {}, 2: {}}

        for emb in embeddings:
            image_dict[emb.image_index][emb.transform_type] = emb.filename

        # Similarities: Agrupar por transform_type
        similarities = SimilarityMetricResult.objects.filter(comparison=session)
        similarity_block = {}

        for sim in similarities:
            similarity_block[sim.transform_type] = {
                "files": [sim.file_1, sim.file_2],
                "similarity": round(sim.similarity_score, 4)
            }

        # Armar respuesta
        return {
            "imagen_1": image_dict[1],
            "imagen_2": image_dict[2],
            "similitud": similarity_block
        }
