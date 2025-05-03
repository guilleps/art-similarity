from rest_framework import serializers
from api.domain.serializers import ImageAnalyzedSerializer, SimilarityResultSerializer

class BatchResultSerializer(serializers.Serializer):
    analyzed_image = ImageAnalyzedSerializer()
    similarities = SimilarityResultSerializer(many=True)