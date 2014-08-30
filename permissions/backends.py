from django.contrib.auth.backends import ModelBackend

from tracker.models import Project
from permissions.models import GlobalPermission


def user_has_perm(user, perm, perms):
    for p in perms:
        # this perm allow that action and the user is concerned by this perm
        if hasattr(p, perm) and getattr(p, perm) and p.granted_to(user):
            return True


class Backend(ModelBackend):

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
