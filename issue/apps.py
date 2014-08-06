from django.apps import AppConfig


class IssueConfig(AppConfig):

    name = 'issue'
    verbose_name = "Issue Tracker"

    def ready(self):
        import issue.signals
