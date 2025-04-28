from django.contrib import admin
from .models import ImageAnalyzed, SimilarityResult

# Register your models here.
admin.site.register(ImageAnalyzed)
admin.site.register(SimilarityResult)