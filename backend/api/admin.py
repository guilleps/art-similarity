from django.contrib import admin
from api.domain.models import ImageAnalyzed, SimilarityResult

# Register your models here.
admin.site.register(ImageAnalyzed)
admin.site.register(SimilarityResult)