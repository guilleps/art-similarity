from django.db import models
from .comparison_session import ImageComparisonSession

class TransformType(models.TextChoices):
    CONTRAST = "contrast", "Contrast"
    TEXTURE = "texture", "Texture"
    HEATMAP = "heat_color_map", "Heat Color Map"
    HSV_HUE = "hsv_hue", "HSV Hue"
    HSV_SATURATION = "hsv_saturation", "HSV Saturation"
    HSV_VALUE = "hsv_value", "HSV Value"

class SimilarityMetricResult(models.Model):
    comparison = models.ForeignKey(ImageComparisonSession, on_delete=models.CASCADE, related_name="similarities")
    transform_type = models.CharField(max_length=20, choices=TransformType.choices)
    similarity_score = models.FloatField()
    file_1 = models.CharField(max_length=255)
    file_2 = models.CharField(max_length=255)

    class Meta:
        unique_together = ('comparison', 'transform_type')

    def __str__(self):
        return f"{self.comparison_id} - {self.transform_type} = {self.similarity_score:.4f}"
