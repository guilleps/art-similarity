from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application import UploadBatchUseCase
from api.domain.serializers import ImageAnalyzedSerializer

class UploadBatchAPI(APIView):
    def post(self, request, *args, **kwargs):
        image_files = request.FILES.getlist('images')
        if not image_files:
            return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = UploadBatchUseCase()
            analyzed_images = use_case.execute(image_files)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        analyzed_images_serializer = ImageAnalyzedSerializer(analyzed_images, many=True)

        return Response({
            'uploaded_images': analyzed_images_serializer.data
        }, status=status.HTTP_201_CREATED)
    