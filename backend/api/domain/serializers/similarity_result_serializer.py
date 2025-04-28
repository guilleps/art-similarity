from rest_framework import serializers
from api.domain.models import SimilarityResult

class SimilarityResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarityResult
        fields = ['similar_image_id', 'similar_image_url', 'similarity_percentage']
