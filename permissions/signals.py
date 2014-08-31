from django.db.models.signals import pre_delete
from django.dispatch import receiver

from accounts.models import *
from permissions.models import *


"""
As permissions objects do not use a foreign key but instead an integer field
on the foreign object id, we can rely on database cascade deletion to delete
outaded permissions and we have to do it our-self.
"""


@receiver(pre_delete, sender=User, dispatch_uid="clean_user_perms")
def clean_user_perms(sender, instance, **kwargs):
    # Clean global permissions
    perms = GlobalPermission.objects.filter(grantee_id=instance.id,
            grantee_type=GlobalPermission.GRANTEE_USER)
    perms.delete()
    # Clean project permissions
    perms = ProjectPermission.objects.filter(grantee_id=instance.id,
            grantee_type=GlobalPermission.GRANTEE_USER)
    perms.delete()


@receiver(pre_delete, sender=Group, dispatch_uid="clean_group_perms")
def clean_group_perms(sender, instance, **kwargs):
    # Clean global permissions
    perms = GlobalPermission.objects.filter(grantee_id=instance.id,
            grantee_type=GlobalPermission.GRANTEE_GROUP)
    perms.delete()
    # Clean project permissions
    perms = ProjectPermission.objects.filter(grantee_id=instance.id,
            grantee_type=GlobalPermission.GRANTEE_GROUP)
    perms.delete()


@receiver(pre_delete, sender=Team, dispatch_uid="clean_team_perms")
def clean_team_perms(sender, instance, **kwargs):
    print(instance)
    print(instance.id)
    # Clean global permissions
    perms = GlobalPermission.objects.filter(grantee_id=instance.id,
            grantee_type=GlobalPermission.GRANTEE_TEAM)
    print(perms)
    perms.delete()
    # Clean project permissions
    perms = ProjectPermission.objects.filter(grantee_id=instance.id,
            grantee_type=GlobalPermission.GRANTEE_TEAM)
    perms.delete()
