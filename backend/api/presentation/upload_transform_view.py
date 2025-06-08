from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from api.application import UploadTransformedImagesUseCase
import os

SECRET_KEY = os.environ.get('UPLOAD_SECRET_KEY')

ALLOWED_IMAGE_FORMATS = ['JPEG', 'JPG']

@parser_classes([MultiPartParser, FormParser])
@extend_schema(
    summary="Upload two images for transformation, encoding, and comparison.",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'image_1': {'type': 'string', 'format': 'binary'},
                'image_2': {'type': 'string', 'format': 'binary'},
            },
            'required': ['image_1', 'image_2']
        },
    },
    responses={
        201: OpenApiResponse(description="`comparison_id` generated. The new comparison session."),
        400: OpenApiResponse(description="Error if any of the image files are missing."),
        403: OpenApiResponse(description="Forbidden. Invalid or missing secret key."),
        404: OpenApiResponse(description="Not found."),
        500: OpenApiResponse(description="Internal processing error."),
    },
    parameters=[
        OpenApiParameter(
            name='X-Secret-Key', 
            type=str, 
            location=OpenApiParameter.HEADER, 
            description='The secret key required for accessing this endpoint.'
        )
    ]
)
class UploadTransformedImagesAPI(APIView):  
    """ 
    **Request body parameters:**
    - `image_1` (file): First image (required).
    - `image_2` (file): Second image (required).
    """
    parser_classes = [MultiPartParser]
    
    def post(self, request, *args, **kwargs):

        secret_key = request.headers.get('X-Secret-Key')

        if secret_key != SECRET_KEY:
            return Response({'error': 'Forbidden. Invalid or missing secret key.'}, status=403)

        # Obtener las imágenes del request
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')

        # Validar que se hayan recibido ambas imágenes
        if not image_1 or not image_2:
            return Response({"error": "Both images ('image_1' and 'image_2') must be included."}, status=400)

        try:
            # Llamada al caso de uso para procesar las imágenes
            use_case = UploadTransformedImagesUseCase()
            comparison_id = use_case.execute(image_1, image_2)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"comparison_id": str(comparison_id)}, status=201)
    