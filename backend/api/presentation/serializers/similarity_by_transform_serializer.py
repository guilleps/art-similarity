from rest_framework import serializers

class SimilarityByTransformItemSerializer(serializers.Serializer):
    pair = serializers.IntegerField(
        help_text="Sequential pair number (starting from 1)"
    )
    value = serializers.FloatField(
        help_text="Similarity score for the selected transformation"
    )