from django.db import models
from .image_analyzed import ImageAnalyzed

class SimilarityResult(models.Model):
    analyzed_image = models.ForeignKey(ImageAnalyzed, related_name='similarities', on_delete=models.CASCADE)
    similar_image_id = models.CharField(max_length=255)
    similar_image_url = models.URLField()
    similarity_percentage = models.IntegerField()

    def __str__(self):
        return f"Similarity {self.similarity_percentage} to {self.analyzed_image.id}"
