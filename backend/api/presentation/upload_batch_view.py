from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application import UploadBatchUseCase
from api.domain.serializers import BatchResultSerializer

class UploadBatchAPI(APIView):
    def post(self, request, *args, **kwargs):
        image_files = request.FILES.getlist('images')
        if not image_files:
            return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = UploadBatchUseCase()
            analyzed_images = use_case.execute(image_files)
            structured_data = [
                { "analyzed_image": img, "similarities": sims }
                for img, sims in analyzed_images
            ]
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = BatchResultSerializer(structured_data, many=True)

        return Response({
            'results': serializer.data
        }, status=status.HTTP_201_CREATED)
    