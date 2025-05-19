import time

from api.infrastructure.services import upload_image_to_cloudinary, generate_embbeding, generate_id_for_image, search_similar_images
from api.domain.models import ImageAnalyzed, SimilarityResult

class UploadImageUseCase:
    def execute(self, image_file):
        start_time = time.time()

        image_bytes = image_file.read()
        image_file.seek(0)

        embedding = generate_embbeding(image_bytes)
        cloudinary_result = upload_image_to_cloudinary(image_bytes)

        image_id = generate_id_for_image() # no se almacena en pinecone
        similar_images = search_similar_images(embedding)

        processing_time = time.time() - start_time

        analyzed_image = ImageAnalyzed.objects.create(
            id=image_id,
            url=cloudinary_result['secure_url'],
            processing_time=processing_time
        )

        similarity_results = []
        for sim in similar_images:
            similarity = SimilarityResult(
                analyzed_image=analyzed_image,
                similar_image_id=sim.get('id'),
                similar_image_url=sim.get('image_url'),
                similarity_percentage=sim.get('similarity_percentage')
            )
            similarity_results.append(similarity)

        SimilarityResult.objects.bulk_create(similarity_results)

        return analyzed_image, similarity_results
    