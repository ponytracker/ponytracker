from django.db.models.signals import post_save
from django.dispatch import receiver

from issue.models import Project, Label


@receiver(post_save, sender=Project, dispatch_uid="Default project labels.")
def create_default_project_labels(sender, **kwargs):
    if not kwargs['created']:
        return
    project = kwargs['instance']
    if not project.labels.exists():
        Label(project=project, name='bug', color='#FF0000').save()
        Label(project=project, name='feature', color='#00A000').save()
        Label(project=project, name='documentation', color='#1D3DBE').save()
