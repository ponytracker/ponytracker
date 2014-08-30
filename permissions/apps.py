from django.apps import AppConfig


class PermissionsConfig(AppConfig):

    name = 'permissions'
    verbose_name = 'Permissions'

    def ready(self):
        import permissions.signals
