from django.db import models

# Create your models here.
class ImageAnalyzed(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Analyzed Image {self.id}"
