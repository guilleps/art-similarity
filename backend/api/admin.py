from django.contrib import admin
from api.domain.models import ImageComparisonSession,TransformedImageEmbedding, SimilarityMetricResult

# Register your models here.
admin.site.register(ImageComparisonSession)
admin.site.register(TransformedImageEmbedding)
admin.site.register(SimilarityMetricResult)
