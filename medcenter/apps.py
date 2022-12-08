from django.apps import AppConfig


class MedcenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medcenter'

    def ready(self):
        import medcenter.signals
