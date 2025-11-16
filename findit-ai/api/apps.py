# File: api/apps.py

from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """
        This method is called when the app registry is fully populated.
        This is the correct place to import your signals.
        """
        import api.signals