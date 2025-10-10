import os
from typing import List, Dict, Any, Tuple
from transformations.infrastructure.services import (
    CloudStorageService,
    ComparisonSessionService,
    TransformationService,
    EmbeddingService,
    SimilarityService,
)


class UploadTransformedImagesUseCase:
    def __init__(self):
        self.cloud_storage = CloudStorageService()
        self.comparison_session_service = ComparisonSessionService()
        self.transformation_service = TransformationService()
        self.embedding_service = EmbeddingService()
        self.similarity_service = SimilarityService()

    def find_image_pairs(self, base_dir: str) -> List[Tuple[str, str]]:
        image_pairs = []
        for dir_name in sorted(os.listdir(base_dir)):
            dir_path = os.path.join(base_dir, dir_name)
            if not os.path.isdir(dir_path):
                continue

            images = []
            for file in os.listdir(dir_path):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    images.append(os.path.join(dir_path, file))
                    if len(images) == 2:
                        break

            if len(images) == 2:
                image_pairs.append((images[0], images[1]))

        return image_pairs

    def process_directory(self, base_dir: str) -> List[Dict[str, Any]]:
        results = []
        image_pairs = self.find_image_pairs(base_dir)

        for img1_path, img2_path in image_pairs:
            try:
                with open(img1_path, "rb") as f1, open(img2_path, "rb") as f2:
                    image_urls = self.cloud_storage.upload_images([f1, f2])

                session = self.comparison_session_service.create_session(image_urls)
                transformed = self.transformation_service.transform_images(*image_urls)
                embeddings = self.embedding_service.process_and_save_embeddings(
                    session, transformed
                )
                self.similarity_service.compute_and_save(session, embeddings)

                results.append(
                    {
                        "session_id": str(session.id),
                        "image1": image_urls[0],
                        "image2": image_urls[1],
                        "status": "success",
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "image1": img1_path,
                        "image2": img2_path,
                        "status": "error",
                        "error": str(e),
                    }
                )

        return results

    def execute(self, base_directory: str) -> List[Dict[str, Any]]:
        if not os.path.isdir(base_directory):
            raise ValueError(f"Directory not found: {base_directory}")

        return self.process_directory(base_directory)
