from concurrent.futures import ThreadPoolExecutor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import ImageAnalyzed, SimilarityResult

from ..services.cloudinary_service import upload_image_to_cloudinary
from ..services.embedding_service import generate_embbeding, generate_id_for_image
from ..services.pinecone_service import store_embedding, search_similar_images

class UploadImageAPI(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_bytes = image_file.read() # guardamos el contenido en memoria
        image_file.seek(0)
        
        try:
            with ThreadPoolExecutor() as executor:
                future_cloudinary = executor.submit(upload_image_to_cloudinary, image_file)
                future_embedding = executor.submit(generate_embbeding, image_bytes)
                
                cloudinary_result = future_cloudinary.result()
                embedding = future_embedding.result()
        except Exception as e:
            return Response({'error': f'Error during processing parallel: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        image_id = generate_id_for_image()

        try:
            store_embedding(image_id, embedding, cloudinary_result['secure_url'])
            similar_images = search_similar_images(embedding)
        except Exception as e:
            return Response({'error': f'Pinecone error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        analyzed_image = ImageAnalyzed.objects.create(
            id=image_id,
            url=cloudinary_result['secure_url']
        )

        for sim in similar_images:
            SimilarityResult.objects.create(
                analyzed_image=analyzed_image,
                similar_image_id=sim.get('id'),
                similar_image_url=sim.get('image_url'),
                similarity_percentage=sim.get('similarity_percentage')
            )   

        return Response({
            'image_analize': {
                'id': analyzed_image.id,
                'url': analyzed_image.url
            },
            'similarities': similar_images
        }, status=status.HTTP_201_CREATED)


class UploadImageBatchAPI(APIView):
    def post(self, request, *args, **kwargs):
        images_files = request.FILES.getlist('images')
        if not images_files:
            return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = []

        for image_file in images_files:
            image_bytes = image_file.read()
            image_file.seek(0)
        
            try:
                cloudinary_result = upload_image_to_cloudinary(image_file)
            except Exception as e:
                return Response({'error': f'Cloudinary error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            image_id = generate_id_for_image()

            embedding = generate_embbeding(image_bytes)

            try:
                store_embedding(image_id, embedding, cloudinary_result['secure_url'])
                image_name = image_file.name
                results.append({"image": image_name, "secure_url": cloudinary_result['secure_url']})
            except Exception as e:
                return Response({'error': f'Pinecone error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(results, status=status.HTTP_201_CREATED)

