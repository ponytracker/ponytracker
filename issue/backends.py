from django.contrib.auth.backends import ModelBackend

from issue.models import *


def user_has_perm(user, perm, perms):
    for p in perms:
        # this permission allow that action and the user is concerned by this permission
        if hasattr(p, perm) and getattr(p, perm) and p.granted_to(user):
            return True

class ProjectBackend(ModelBackend):

    def has_perm(self, user, perm, obj=None):

        if isinstance(obj, Project):
            # get permissions concerning this project
            perms = obj.permissions.all()
            if user_has_perm(user, perm, perms):
                return True

        # get global permissions
        perms = GlobalPermission.objects.all()
        if user_has_perm(user, perm, perms):
            return True

        return False
