from django.apps import AppConfig
from transformations.infrastructure.config.logging_config import setup_logging


class FeatureExtractorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transformations'

    def ready(self):
        setup_logging()