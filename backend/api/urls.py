
from django.urls import path
from .views.views import UploadImageAPI

urlpatterns = [
    path('api/upload/', UploadImageAPI.as_view(), name='upload_image')
]

