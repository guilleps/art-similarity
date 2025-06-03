from django.apps import AppConfig
from api.infrastructure.config.logging_config import setup_logging

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        setup_logging()
