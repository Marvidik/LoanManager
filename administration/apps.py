from django.apps import AppConfig


class AdministrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administration'

    def ready(self):
        import administration.signals  # Import your signals module


