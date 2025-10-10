from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformations.application.upload_transformed_images_usecase import (
    UploadTransformedImagesUseCase,
)
import os
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from transformations.application import UploadTransformedImagesUseCase

SECRET_KEY = os.environ.get("UPLOAD_SECRET_KEY")


@extend_schema(
    summary="Upload two images for transformation, encoding, and comparison.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "directory_path": {
                    "type": "string",
                    "description": "Absolute path to the directory containing image pairs",
                }
            },
        }
    },
    parameters=[
        OpenApiParameter(
            name="X-Secret-Key",
            type=str,
            location=OpenApiParameter.HEADER,
            description="The secret key required for accessing this endpoint.",
        ),
    ],
    responses={
        201: OpenApiResponse(
            description="`comparison_id` generated. The new comparison session."
        ),
        400: OpenApiResponse(
            description="Error if any of the image files are missing."
        ),
        403: OpenApiResponse(description="Forbidden. Invalid or missing secret key."),
        404: OpenApiResponse(description="Not found."),
        500: OpenApiResponse(description="Internal processing error."),
    },
)
class UploadTransformedImagesAPI(APIView):
    """
    **Request body parameters:**
    - `path` (string): Path to the directory containing the images (required).
    """

    def post(self, request, *args, **kwargs):

        secret_key = request.headers.get("X-Secret-Key")
        if secret_key != SECRET_KEY:
            return Response(
                {"error": "Forbidden. Invalid or missing secret key."},
                status=status.HTTP_403_FORBIDDEN,
            )

        directory_path = request.data.get("directory_path")

        if not directory_path:
            return Response(
                {"error": "directory_path parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not os.path.isabs(directory_path):
            return Response(
                {"error": "Please provide an absolute path to the directory"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not os.path.isdir(directory_path):
            return Response(
                {"error": f"Directory not found: {directory_path}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            use_case = UploadTransformedImagesUseCase()
            results = use_case.execute(directory_path)

            success_count = sum(1 for r in results if r["status"] == "success")
            error_count = len(results) - success_count

            return Response(
                {
                    "total_pairs_processed": len(results),
                    "successful": success_count,
                    "failed": error_count,
                    "results": results,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
