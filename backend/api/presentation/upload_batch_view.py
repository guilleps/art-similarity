from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application import UploadBatchUseCase

class UploadBatchAPI(APIView):
    def post(self, request, *args, **kwargs):
        image_files = request.FILES.getlist('images')
        if not image_files:
            return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = UploadBatchUseCase()
            results = use_case.execute(image_files)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'results': results
        }, status=status.HTTP_201_CREATED)
    