from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework import status

class CarbonFootprintView(APIView):
    def get(self, request):
        bytes = 317070
        green = 1
        
        try:
            response = requests.get(
                f'https://api.websitecarbon.com/data?bytes={bytes}&green={green}'
            )
            response.raise_for_status()
            return Response(response.json())
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': 'Error fetching CO₂ data', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
