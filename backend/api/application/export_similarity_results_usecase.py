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
        # First pass to get all unique transform types for the header
        sessions = self._get_sessions_with_related_data()
        transform_types = set()
        
        for session in sessions:
            pair_data = self._process_session_data(session)
            for key in pair_data:
                if key not in ["image_1", "image_2"]:
                    transform_types.add(key)
        
        # Sort transform types for consistent ordering
        transform_types = sorted(transform_types)
        
        # Write header
        writer = csv.writer(response_object)
        writer.writerow(["pair_id"] + list(transform_types))
        
        # Second pass to write data
        for pair_id, session in enumerate(sessions, start=1):
            pair_data = self._process_session_data(session)
            self._write_session_to_csv(writer, pair_id, pair_data, transform_types)
            
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

    def _write_session_to_csv(self, writer, pair_id, pair_data, transform_types):
        # Initialize row with just pair_id
        row = [pair_id]
        
        # Add similarity scores in the same order as transform_types
        for transform_type in transform_types:
            if transform_type in pair_data:
                row.append(str(pair_data[transform_type].get("similarity", "")))
            else:
                row.append("")
                
        writer.writerow(row)
