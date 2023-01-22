from django.apps import AppConfig


class DhuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dhule'

    def ready(self):
        import dhule.signals