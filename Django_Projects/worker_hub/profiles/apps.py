from django.apps import AppConfig
import logging


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

        
    def ready(self):
        import profiles.signals
        logging.info("Profiles signals registered successfully.")
