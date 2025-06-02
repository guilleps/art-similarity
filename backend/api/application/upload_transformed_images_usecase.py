import os
import requests
from sklearn.metrics.pairwise import cosine_similarity
import json
from api.domain.models import ImageComparisonSession, TransformedImageEmbedding, SimilarityMetricResult
from api.infrastructure.services import upload_image_to_cloudinary, generate_embedding

TRANSFORM_SERVICE_URL = os.environ.get("TRANSFORM_SERVICE_URL")

class UploadTransformedImagesUseCase:
    def execute(self, local_path: str) -> str:
        try:
            # 1. Buscar imágenes en carpeta local
            image_files = [f for f in os.listdir(local_path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
            if len(image_files) != 2:
                raise ValueError("La carpeta debe contener exactamente 2 imágenes")
            image_files.sort()
        except Exception as e:
            print("Error al buscar imágenes en la carpeta local")
            raise

        image_files.sort()  # orden alfabético para tener imagen_1 e imagen_2
        
        try:
            # 2. Subir imágenes a Cloudinary
            original_urls = []
            for image in image_files:
                full_path = os.path.join(local_path, image)
                result = upload_image_to_cloudinary(full_path)
                original_urls.append(result["secure_url"])
        except Exception as e:
            print("Error al subir imágenes originales a Cloudinary")
            raise

        try:
            # 3. Crear sesión de comparación
            session = ImageComparisonSession.objects.create()
        except Exception as e:
            print("Error al crear la sesión de comparación")
            raise

        try:
            # 4. Guardar originales
            for i, url in enumerate(original_urls, start=1):
                TransformedImageEmbedding.objects.create(
                    comparison=session,
                    image_index=i,
                    transform_type="original_image",
                    filename=url,
                    embedding_url=url
                )
        except Exception as e:
            print("Error al guardar las imágenes originales en la BD")
            raise

        try:
            # 5. Llamar al servicio de transformacion
            response = requests.post(f"{TRANSFORM_SERVICE_URL}/transform", json={
                "image_1_url": original_urls[0],
                "image_2_url": original_urls[1]
            })
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print("Error en la llamada al microservicio de transformaciones")
            raise

        embedding_lookup = {1: {}, 2: {}}  # image_index => {transform_type: embedding_url}

        for index, key in enumerate(["imagen_1", "imagen_2"], start=1):
            for transform_type, image_url in data[key].items():
                if transform_type == "original_image":
                    continue

                image_bytes = requests.get(image_url).content
                embedding_url = generate_embedding(image_bytes)  # microservicio CNN CLIP

                TransformedImageEmbedding.objects.create(
                    comparison=session,
                    image_index=index,
                    transform_type=transform_type,
                    image_url=image_url,
                    embedding_url=embedding_url
                )

                # Guardar para similitud
                embedding_lookup[index][transform_type] = embedding_url

        try:
            # 7. Calcular similitud y guardar
            for transform_type in embedding_lookup[1]:
                url_1 = embedding_lookup[1][transform_type]
                url_2 = embedding_lookup[2][transform_type]

                try:
                    emb_1 = requests.get(url_1).json()
                except json.JSONDecodeError:
                    emb_1 = json.loads(requests.get(url_1).content.decode('utf-8'))

                try:
                    emb_2 = requests.get(url_2).json()
                except json.JSONDecodeError:
                    emb_2 = json.loads(requests.get(url_2).content.decode('utf-8'))

                similarity = cosine_similarity([emb_1], [emb_2])[0][0]

                SimilarityMetricResult.objects.create(
                    comparison=session,
                    transform_type=transform_type,
                    similarity_score=similarity,
                    file_1=url_1,
                    file_2=url_2
                )
        except Exception as e:
            print("Error al calcular o guardar la similitud de transformaciones")
            raise

        print(f"Sesión completada correctamente: {session.id}")
        return str(session.id)
