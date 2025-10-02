import csv
from api.domain.models import ImageComparisonSession


class ExportSimilarityResultsUseCase:
    def exportToJSON(self):
        output = {"pair": {}}
        sessions = self._get_sessions_with_related_data()

        for idx, session in enumerate(sessions, start=1):
            pair_data = self._process_session_data(session)
            output["pair"][str(idx)] = pair_data

        return output

    def exportToCSV(self, response_object):
        writer = csv.writer(response_object)
        writer.writerow(
            ["pair_id", "image_1", "image_2", "transform_type", "similarity_score"]
        )

        sessions = self._get_sessions_with_related_data()

        for pair_id, session in enumerate(sessions, start=1):
            pair_data = self._process_session_data(session)
            self._write_session_to_csv(writer, pair_id, pair_data)

        return response_object

    def _get_sessions_with_related_data(self):
        return ImageComparisonSession.objects.prefetch_related(
            "similarities", "transformedimageembedding_set"
        ).order_by("created_at")

    def _process_session_data(self, session):
        embeddings = session.transformedimageembedding_set.all()
        similarities = session.similarities.all()

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

        pair_data = {"image_1": image_1_url, "image_2": image_2_url}

        for sim in similarities:
            image_1_trans = transform_lookup.get((1, sim.transform_type), "")
            image_2_trans = transform_lookup.get((2, sim.transform_type), "")

            pair_data[sim.transform_type] = {
                "files": {"image_1": image_1_trans, "image_2": image_2_trans},
                "similarity": round(sim.similarity_score, 4),
            }

        return pair_data

    def _write_session_to_csv(self, writer, pair_id, pair_data):
        image_1 = pair_data["image_1"]
        image_2 = pair_data["image_2"]

        for transform_type, transform_data in pair_data.items():
            if transform_type not in ["image_1", "image_2"]:
                similarity = transform_data.get("similarity", "")
                writer.writerow([pair_id, image_1, image_2, transform_type, similarity])
