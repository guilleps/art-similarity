from api.domain.models import ImageComparisonSession
from api.infrastructure.config import create_async_tracker
import logging

logger = logging.getLogger(__name__)


class GetAllSimilarityResultsRawUseCase:
    def execute(self):
        tracker = create_async_tracker(
            filename="emissions_get_all_similarity_raw_usecase.csv"
        )
        import asyncio
        asyncio.run(tracker.start())

        try:
            return self._process_results()
        finally:
            asyncio.run(tracker.stop_background())

    async def execute_async(self):
        tracker = create_async_tracker(
            filename="emissions_get_all_similarity_raw_usecase.csv"
        )
        await tracker.start()

        try:
            results = await self._process_results_async()
            logger.info(f"Processed {len(results)} results asynchronously")
            return results
        finally:
            await tracker.stop_background()

    def _process_results(self):
        results = []

        sessions = ImageComparisonSession.objects.prefetch_related(
            "similarities", "transformedimageembedding_set"
        ).order_by("created_at")

        for session in sessions:
            embedding_lookup = {}
            for emb in session.transformedimageembedding_set.all():
                embedding_lookup[emb.embedding_url] = emb

            similarity_block = {}
            for sim in session.similarities.all():
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
                    "texture_transformation": similarity_block.get("texture", {}).get(
                        "similarity"
                    ),
                    "contrast_transformation": similarity_block.get("contrast", {}).get(
                        "similarity"
                    ),
                }
            )

        return results

    async def _process_results_async(self):
        results = []

        sessions = ImageComparisonSession.objects.prefetch_related(
            "similarities", "transformedimageembedding_set"
        ).order_by("created_at")

        async for session in sessions:
            embeddings = [emb async for emb in session.transformedimageembedding_set.all()]
            similarities = [sim async for sim in session.similarities.all()]

            embedding_lookup = {}
            for emb in embeddings:
                embedding_lookup[emb.embedding_url] = emb

            similarity_block = {}
            for sim in similarities:
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
                    "texture_transformation": similarity_block.get("texture", {}).get(
                        "similarity"
                    ),
                    "contrast_transformation": similarity_block.get("contrast", {}).get(
                        "similarity"
                    ),
                }
            )

        return results