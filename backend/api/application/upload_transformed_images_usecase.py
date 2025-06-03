from api.infrastructure.services import (
    ImageLoaderService,
    CloudStorageService,
    ComparisonSessionService,
    TransformationService,
    EmbeddingService,
    SimilarityService
)

class UploadTransformedImagesUseCase:
    def __init__(self):
        self.image_loader = ImageLoaderService()
        self.cloud_storage = CloudStorageService()
        self.comparison_session_service = ComparisonSessionService()
        self.transformation_service = TransformationService()
        self.embedding_service = EmbeddingService()
        self.similarity_service = SimilarityService()

    def execute(self, local_path: str) -> str:
        filenames = self.image_loader.load_images(local_path)
        image_urls = self.cloud_storage.upload_images(local_path, filenames)
        session = self.comparison_session_service.create_session(image_urls)
        transformed = self.transformation_service.transform_images(*image_urls)
        embeddings = self.embedding_service.process_and_save_embeddings(session, transformed)
        self.similarity_service.compute_and_save(session, embeddings)
        return str(session.id)
    