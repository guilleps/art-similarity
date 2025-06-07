from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.application import GetSimilarityResultUseCase

class GetSimilarityResultAPI(APIView):
    """
    Obtener los resultados de similitud de un par específico de imagenes.
    
    **Parámetros en la URL:**
    - `comparison_id` (UUID): ID de la sesión de comparación (requerido).

    **Respuestas:**
    - 200: Devuelve los resultados de similitud entre las imágenes comparadas.
    - 404: Si no se encuentra la sesión de comparación con el `comparison_id`.
    
    **Ejemplo de uso:**
    - Endpoint: `/api/get-similarity/{comparison_id}/`
    - Método: `GET`
    - Respuesta de ejemplo: 
      ```json
      {
        "comparison_id": "abcd-1234-xyz",
        "imagen_1": { "original_image": "image_url", "contrast": "contrast_image_url" },
        "imagen_2": { "original_image": "image_url", "contrast": "contrast_image_url" },
        "similitud": { "contrast": { "files": ["image_1_url", "image_2_url"], "similarity": 0.95 } }
      }
      ```
    """
    def get(self, request, comparison_id, *args, **kwargs):
        try:
            use_case = GetSimilarityResultUseCase()
            result = use_case.execute(comparison_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)
