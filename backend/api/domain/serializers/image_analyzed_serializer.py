from rest_framework import serializers
from api.domain.models import ImageAnalyzed

class ImageAnalyzedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnalyzed
        fields = ['id', 'url', 'created_at']