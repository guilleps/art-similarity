import os
import requests
from api.domain.models import ImageComparisonSession, TransformedImageEmbedding, SimilarityMetricResult
from api.infrastructure.services import upload_image_to_cloudinary


class UploadTransformedImagesUseCase:
    def execute(self, local_path: str) -> str:
        # 1. Buscar imágenes en carpeta local
        image_files = [f for f in os.listdir(local_path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        if len(image_files) != 2:
            raise ValueError("La carpeta debe contener exactamente 2 imágenes")

        image_files.sort()  # orden alfabético para tener imagen_1 e imagen_2
        original_urls = []

        # 2. Subir cada imagen original a Cloudinary
        for image in image_files:
            full_path = os.path.join(local_path, image)
            image_upload_result = upload_image_to_cloudinary(full_path) # devuelve secure_url de la imagen original
            original_urls.append(image_upload_result["secure_url"])

        # 3. Crear sesión
        session = ImageComparisonSession.objects.create()

        # 4. Guardar en BD las originales
        for i, url in enumerate(original_urls, start=1):
            TransformedImageEmbedding.objects.create(
                comparison=session,
                image_index=i,
                transform_type="original_image",
                filename=url.split("/")[-1],
                embedding_url=url
            )

        # 5. Llamar al microservicio de transformacion
        response = requests.post("http://localhost:8001/transform", json={
            "image_1_url": original_urls[0],
            "image_2_url": original_urls[1]
        })

        if response.status_code != 200:
            raise Exception("Error en el microservicio externo")

        data = response.json()

        # 6. Guardar transformaciones y embeddings
        for index, key in enumerate(["imagen_1", "imagen_2"], start=1):
            for transform_type, embedding_url in data[key].items():
                if transform_type == "original_image":
                    continue  # ya guardamos
                TransformedImageEmbedding.objects.create(
                    comparison=session,
                    image_index=index,
                    transform_type=transform_type,
                    filename=embedding_url.split("/")[-1],
                    embedding_url=embedding_url
                )

        # 7. Guardar similitudes
        for transform_type, values in data["similitud"].items():
            SimilarityMetricResult.objects.create(
                comparison=session,
                transform_type=transform_type,
                similarity_score=values["similarity"],
                file_1=values["files"][0],
                file_2=values["files"][1]
            )

        return str(session.id)
