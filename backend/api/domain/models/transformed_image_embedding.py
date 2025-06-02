from django.db import models
from .comparison_session import ImageComparisonSession

class TransformedImageEmbedding(models.Model):
    TRANSFORM_CHOICES = [
        ('contrast', 'Contrast'),
        ('texture', 'Texture'),
        ('heat_color_map', 'Heat Color Map'),
        ('hsv_hue', 'HSV Hue'),
        ('hsv_saturation', 'HSV Saturation'),
        ('hsv_value', 'HSV Value'),
    ]

    comparison = models.ForeignKey(ImageComparisonSession, on_delete=models.CASCADE, related_name="embeddings")
    image_index = models.IntegerField()  # 1 o 2
    transform_type = models.CharField(max_length=20, choices=TRANSFORM_CHOICES)
    image_url = models.URLField()
    embedding_url = models.URLField()
    filename = models.CharField(max_length=255)

    class Meta:
        unique_together = ('comparison', 'image_index', 'transform_type')

    def __str__(self):
        return f"{self.comparison_id} - Img{self.image_index} - {self.transform_type}"