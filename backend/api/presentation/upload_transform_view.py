from rest_framework.views import APIView
from rest_framework.response import Response

from api.application import UploadTransformedImagesUseCase

class UploadTransformedImagesAPI(APIView):
    def post(self, request, *args, **kwargs):
        local_path = request.data.get("local_dir_path")
        if not local_path:
            return Response({"error": "Debe incluirse el campo local_dir_path"}, status=400)

        try:
            use_case = UploadTransformedImagesUseCase()
            comparison_id = use_case.execute(local_path)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"comparison_id": str(comparison_id)}, status=201)