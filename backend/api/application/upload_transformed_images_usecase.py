from api.infrastructure.services import (
    CloudStorageService,
    ComparisonSessionService,
    TransformationService,
    EmbeddingService,
    SimilarityService
)

class UploadTransformedImagesUseCase:
    def __init__(self):
        self.cloud_storage = CloudStorageService()
        self.comparison_session_service = ComparisonSessionService()
        self.transformation_service = TransformationService()
        self.embedding_service = EmbeddingService()
        self.similarity_service = SimilarityService()

    def execute(self, image_1, image_2) -> str:
        image_urls = self.cloud_storage.upload_images([image_1, image_2])
        session = self.comparison_session_service.create_session(image_urls)
        transformed = self.transformation_service.transform_images(*image_urls)
        embeddings = self.embedding_service.process_and_save_embeddings(session, transformed)
        self.similarity_service.compute_and_save(session, embeddings)
        return str(session.id)
    