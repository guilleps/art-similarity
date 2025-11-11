from api.domain.models import ImageComparisonSession
from api.infrastructure.config import create_async_tracker


class GetSimilarityResultsPagUseCase:
    async def execute(self, offset=0, limit=10):
        tracker = create_async_tracker(filename="emissions_usecase_paginated.csv")
        await tracker.start()

        try:
            results = await self._process_results(offset, limit)
            return results
        finally:
            await tracker.stop_background()

    async def _process_results(self, offset, limit):
        results = []

        sessions = ImageComparisonSession.objects.prefetch_related(
            "similarities", "transformedimageembedding_set"
        ).order_by("created_at")[offset : offset + limit]

        async for session in sessions:
            similarities = [sim async for sim in session.similarities.all()]
            embeddings = [emb async for emb in session.transformedimageembedding_set.all()]
            
            result = self._build_session_result(
                session, similarities, embeddings
            )
            results.append(result)

        return results

    def _build_session_result(self, session, similarities, embeddings):
        embedding_lookup = {}
        image_dict = {1: {}, 2: {}}
        
        for emb in embeddings:
            embedding_lookup[emb.embedding_url] = emb
            if emb.transform_type == "original_image":
                image_dict[emb.image_index]["original_image"] = emb.embedding_url
            else:
                image_dict[emb.image_index][emb.transform_type] = {
                    "image_transformed": emb.image_url,
                }
        
        similarity_block = {}
        
        for sim in similarities:
            emb1 = embedding_lookup.get(sim.file_1)
            emb2 = embedding_lookup.get(sim.file_2)
            
            similarity_block[sim.transform_type] = {
                "files": [
                    emb1.image_url if emb1 else "",
                    emb2.image_url if emb2 else "",
                ],
                "similarity": round(sim.similarity_score, 4),
            }

        return {
            "comparison_id": str(session.id),
            "created_at": session.created_at,
            "color_heat_map_transformation": similarity_block.get(
                "heat_color_map", {}
            ).get("similarity"),
            "tone_transformation": similarity_block.get("hsv_hue", {}).get(
                "similarity"
            ),
            "saturation_transformation": similarity_block.get("hsv_saturation", {}).get(
                "similarity"
            ),
            "brightness_transformation": similarity_block.get("hsv_value", {}).get(
                "similarity"
            ),
            "texture_transformation": similarity_block.get("texture", {}).get(
                "similarity"
            ),
            "contrast_transformation": similarity_block.get("contrast", {}).get(
                "similarity"
            ),
        }
