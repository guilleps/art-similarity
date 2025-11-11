from api.domain.models import ImageComparisonSession
from api.infrastructure.config import create_tracker_to_emission


class GetAllSimilarityResultsRawUseCase:
    def execute(self):
        tracker = create_tracker_to_emission(
            filename="emissions_get_all_similarity_raw_usecase.csv"
        )
        tracker.start()

        try:
            results = []

            sessions = ImageComparisonSession.objects.prefetch_related(
                "similarities", "transformedimageembedding_set"
            ).order_by(
                "created_at"
            )  # Si quieres invertir, puedes usar created_at ASC

            for session in sessions:
                embedding_lookup = {}
                for emb in session.transformedimageembedding_set.all():
                    embedding_lookup[emb.embedding_url] = emb

                similarity_block = {}
                for sim in session.similarities.all():
                    emb1 = embedding_lookup.get(sim.file_1)
                    emb2 = embedding_lookup.get(sim.file_2)

                    similarity_block[sim.transform_type] = {
                        "similarity": round(sim.similarity_score, 4)
                    }

                results.append(
                    {
                        "comparison_id": str(session.id),
                        "color_heat_map_transformation": similarity_block.get(
                            "heat_color_map", {}
                        ).get("similarity"),
                        "tone_transformation": similarity_block.get("hsv_hue", {}).get(
                            "similarity"
                        ),
                        "saturation_transformation": similarity_block.get(
                            "hsv_saturation", {}
                        ).get("similarity"),
                        "brightness_transformation": similarity_block.get(
                            "hsv_value", {}
                        ).get("similarity"),
                        "texture_transformation": similarity_block.get(
                            "texture", {}
                        ).get("similarity"),
                        "contrast_transformation": similarity_block.get(
                            "contrast", {}
                        ).get("similarity"),
                    }
                )

            return results
        finally:
            tracker.stop()
