from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.application import GetSimilarityResultUseCase

class GetSimilarityResultAPI(APIView):
    def get(self, request, comparison_id, *args, **kwargs):
        try:
            use_case = GetSimilarityResultUseCase()
            result = use_case.execute(comparison_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)
