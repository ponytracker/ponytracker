from issue.models import Project


def projects(request):

    if hasattr(request, 'projects'):
        return {'projects': request.projects}
    else:
        return {}


class PermissionChecker:

    def getattr(self, request, perm, obj=None):
        if request.user.is_authenticated():
            return request.user.has_perm(perm, obj)


class PermWrapper:

    def __init__(self, user):
        self.user = user

    def __getitem__(self, perm):
        return self.user.has_perm(perm)

    def __iter__(self):
        raise TypeError("PermWrapper is not iterable.")

    def __contains__(self, perm):
        return self[perm]


def can_user(request):
    wrapper = PermWrapper(request.user)
    return {'can_user': wrapper}
