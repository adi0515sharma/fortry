from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UserProfilesConfig(AppConfig):
    name = 'HR_user_profiles'

    def ready(self):
        import HR_user_profiles.signals
        from .signals import populate_models
        post_migrate.connect(populate_models, sender=self)
