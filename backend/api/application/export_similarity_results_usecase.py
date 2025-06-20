from api.domain.models import ImageComparisonSession

class ExportSimilarityResultsUseCase:
    def execute(self):
        output = {"par": {}}

        sessions = (
            ImageComparisonSession.objects
            .prefetch_related('similarities', 'transformedimageembedding_set')
            .order_by('created_at')
        )

        for idx, session in enumerate(sessions, start=1):
            embeddings = session.transformedimageembedding_set.all()
            similarities = session.similarities.all()

            # Crear lookup de transformaciones por (image_index, transform_type)
            transform_lookup = {
                (e.image_index, e.transform_type): e.image_url
                for e in embeddings
                if e.transform_type != "original_image"
            }

            original_lookup = {
                e.image_index: e.filename
                for e in embeddings
                if e.transform_type == "original_image"
            }

            image_1_url = original_lookup.get(1, "")
            image_2_url = original_lookup.get(2, "")

            par_data = {
                "image_1": image_1_url,
                "image_2": image_2_url
            }

            for sim in similarities:
                image_1_trans = transform_lookup.get((1, sim.transform_type), "")
                image_2_trans = transform_lookup.get((2, sim.transform_type), "")

                par_data[sim.transform_type] = {
                    "files": {
                        "image_1": image_1_trans,
                        "image_2": image_2_trans
                    },
                    "similarity": round(sim.similarity_score, 4)
                }

            output["par"][str(idx)] = par_data

        return output
