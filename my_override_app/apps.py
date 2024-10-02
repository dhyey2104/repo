from django.apps import AppConfig


class MyOverrideAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_override_app'

    def ready(self):
        print("hellooooo")
        # Import the override function from utils.py
        from .utils import override_methods_globally
        # Call the function to apply save/delete overrides globally
        override_methods_globally()
