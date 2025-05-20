from api.infrastructure.services import upload_image_to_cloudinary, generate_embbeding, generate_id_for_image, store_embedding, search_similar_images
from api.domain.models import ImageAnalyzed, SimilarityResult

class UploadBatchUseCase:
    def execute(self, image_files):
        results = []
        
        for image_file in image_files:
            image_bytes = image_file.read()
            image_file.seek(0)

            embedding = generate_embbeding(image_bytes)
            cloudinary_result = upload_image_to_cloudinary(image_bytes)

            image_id = generate_id_for_image()
            store_embedding(image_id, embedding, cloudinary_result['secure_url'])

            results.append({
                "analyzed_image": {
                    "id": image_id,
                    "url": cloudinary_result['secure_url']
                }
            })

        return results