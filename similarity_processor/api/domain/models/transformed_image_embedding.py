from django.db import models
from .comparison_session import ImageComparisonSession

class TransformType(models.TextChoices):
    ORIGINAL = "original_image", "Original"
    COLOR = "color", "Color"
    CONTRAST = "contrast", "Contraste"
    TEXTURE = "texture", "Textura"
    BRUSH = "brush", "Pincel"
    HEATMAP = "heatmap", "Mapa de calor"

class TransformedImageEmbedding(models.Model):
    comparison = models.ForeignKey(
        ImageComparisonSession, 
        on_delete=models.CASCADE,
        verbose_name="Comparison Session",
        help_text="The comparison session this transformed image embedding belongs to."
    )
    image_index = models.PositiveIntegerField(
        verbose_name="Image Index",
        help_text="1 for the first image, 2 for the second image."
    )  # 1 o 2
    transform_type = models.CharField(
        max_length=50, 
        choices=TransformType.choices,
        default=TransformType.ORIGINAL
    )
    image_url = models.URLField()
    embedding_url = models.URLField()
    filename = models.CharField(max_length=255)

    class Meta:
        unique_together = ('comparison', 'image_index', 'transform_type')

    def __str__(self):
        return f"{self.comparison_id} - Img{self.image_index} - {self.transform_type}"
