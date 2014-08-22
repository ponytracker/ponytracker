from django.db.models.signals import post_save
from django.dispatch import receiver

from issue.models import Project, Label


@receiver(post_save, sender=Project, dispatch_uid="Default project labels.")
def create_default_project_labels(sender, instance, created, **kwargs):
    if not created:
        return
    if not instance.labels.exists():
        Label(project=instance, name='bug', color='#FF0000').save()
        Label(project=instance, name='feature', color='#00A000').save()
        Label(project=instance, name='documentation', color='#1D3DBE').save()
