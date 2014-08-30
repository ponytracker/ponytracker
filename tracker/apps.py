from django.apps import AppConfig


class TrackerConfig(AppConfig):

    name = 'tracker'
    verbose_name = 'Tracker'

    def ready(self):
        import tracker.signals
