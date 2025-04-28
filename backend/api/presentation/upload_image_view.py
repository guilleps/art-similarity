from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application import UploadImageUseCase
from api.domain.serializers import ImageAnalyzedSerializer, SimilarityResultSerializer

class UploadImageAPI(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            use_case = UploadImageUseCase()
            analyzed_image, similarity_results = use_case.execute(image_file)
        except Exception as e:
            return Response({'error': f'Error during processing: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        analyzed_image_serializer = ImageAnalyzedSerializer(analyzed_image)
        similarities_serializer = SimilarityResultSerializer(similarity_results, many=True)

        return Response({
            'image_analize': analyzed_image_serializer.data,
            'similarities': similarities_serializer.data
        }, status=status.HTTP_201_CREATED)
