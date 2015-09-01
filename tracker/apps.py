from django.apps import AppConfig
from django.db.models.signals import post_migrate


class TrackerConfig(AppConfig):

    name = 'tracker'
    verbose_name = 'Tracker'

    def ready(self):
        import tracker.signals
        post_migrate.connect(tracker.signals.create_default_settings, sender=self)
