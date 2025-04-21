from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.cloudinary_service import upload_image_to_cloudinary
from ..services.embedding_service import generate_embbeding, generate_id_for_image
from ..services.pinecone_service import store_embedding

class UploadImageAPI(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_bytes = image_file.read() # guardamos el contenido en memoria
        image_file.seek(0)  # Reset el puntero para que Cloudinary también lo lea correctamente
        
        try:
            cloudinary_result = upload_image_to_cloudinary(image_file)
        except Exception as e:
            return Response({'error': f'Cloudinary error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        image_id = generate_id_for_image()
        embedding = generate_embbeding(image_bytes)

        try:
            store_embedding(image_id, embedding, cloudinary_result['secure_url'])
        except Exception as e:
            return Response({'error': f'Pinecone error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'secure_url': cloudinary_result['secure_url'],
            'embedding': embedding
            # faltan porcentaje calculado, obtener de los response embeddings de la bd vectorial
        }, status=status.HTTP_201_CREATED)
