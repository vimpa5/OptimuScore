from django.apps import AppConfig


class SolapurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'solapur'

    def ready(self):
        import solapur.signals