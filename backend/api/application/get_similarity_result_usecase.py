from api.domain.models import (
    ImageComparisonSession,
    TransformedImageEmbedding,
    SimilarityMetricResult,
)
from django.core.exceptions import ObjectDoesNotExist
import logging
from api.application.prompt_builder import SYSTEM_PROMPT, build_user_prompt, pick_winner
from api.infrastructure.services.llm_client import call_llm_text_only
from api.infrastructure.config import create_tracker_to_emission

class GetSimilarityResultUseCase:
    def execute(self, comparison_id):
        
        tracker = create_tracker_to_emission(filename="emissions_usecase_get_similarity.csv")
        tracker.start()

        try:
            session = ImageComparisonSession.objects.get(id=comparison_id)
        except ObjectDoesNotExist:
            raise ValueError(
                f"No se encontró la sesión de comparación con ID: {comparison_id}"
            )

        try:
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
                        emb2.image_url if emb2 else "",
                    ],
                    "similarity": round(sim.similarity_score, 4),
                }

            base_payload = {
                "comparison_id": str(comparison_id),
                "image_1": image_dict[1],
                "image_2": image_dict[2],
                "similitud": similarity_block,
            }

            return base_payload
        
        finally:
            tracker.stop()

        # LLM analysis with deterministic fallback
        # logger = logging.getLogger(__name__)
        # try:
        #     user_prompt = build_user_prompt(base_payload)
        #     analysis = call_llm_text_only(SYSTEM_PROMPT, user_prompt)
        # except Exception as e:
        #     logger.exception(
        #         f"[LLM Analyze] fallo para comparison_id={comparison_id}: {e}"
        #     )

        #     def label_for(value: float) -> str:
        #         if value >= 0.93:
        #             return "muy similar"
        #         if value >= 0.88:
        #             return "similar"
        #         return "diferente"

        #     t, s = pick_winner(similarity_block)
        #     ranking = sorted(
        #         (
        #             {
        #                 "transform": k,
        #                 "similarity": v["similarity"],
        #                 "label": label_for(v["similarity"]),
        #             }
        #             for k, v in similarity_block.items()
        #         ),
        #         key=lambda x: x["similarity"],
        #         reverse=True,
        #     )

        #     analysis = {
        #         "comparison_id": base_payload["comparison_id"],
        #         "winner": {
        #             "transform": t,
        #             "similarity": s,
        #             "confidence": "low",
        #             "why": "Elegido por mayor similarity (fallback)",
        #         },
        #         "ranking": ranking,
        #         "thresholds": {"very_similar": 0.93, "similar": 0.88},
        #         "notes": "Respuesta generada por heurística; reintentar con LLM.",
        #     }

        # base_payload["analysis"] = analysis

