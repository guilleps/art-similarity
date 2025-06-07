from rest_framework.views import APIView
from rest_framework.response import Response

from api.application import UploadTransformedImagesUseCase

class UploadTransformedImagesAPI(APIView):
    """
    Subir una carpeta con un par de imágenes e inicia el proceso de transformación, codificacion y comparacion.
    
    **Parámetros en el cuerpo de la solicitud:**
    - `local_dir_path` (string): Ruta local de las imágenes que se van a subir (requerido).

    **Respuestas:**
    - 201: `comparison_id` generado. La nueva sesión de comparación.
    - 400: Error si falta el parámetro `local_dir_path` en la solicitud.
    - 500: Error interno en el procesamiento.
    
    **Ejemplo de uso:**
    - Endpoint: `/api/internal/upload-transform/`
    - Método: `POST`
    - Cuerpo: `{ "local_dir_path": "/path/to/images" }`
    """
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