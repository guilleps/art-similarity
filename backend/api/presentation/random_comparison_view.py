from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.domain.models import ImageComparisonSession
import random

class RandomComparisonSessionAPI(APIView):
    def get(self, request, *args, **kwargs):
        sessions = ImageComparisonSession.objects.values_list('id', flat=True)
        if not sessions:
            return Response({"error": "No hay sesiones registradas"}, status=status.HTTP_404_NOT_FOUND)

        random_id = random.choice(sessions)
        return Response({"comparison_id": str(random_id)}, status=status.HTTP_200_OK)
