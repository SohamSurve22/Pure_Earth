from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """Initialize app when Django starts."""
        # Import template tags to ensure they are registered
        import core.templatetags.core_extras
