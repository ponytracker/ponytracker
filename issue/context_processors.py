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

    def __init__(self, user, project):
        self.user = user
        self.project = project

    def __getitem__(self, perm):
        return self.user.has_perm(perm, self.project)

    def __iter__(self):
        raise TypeError("PermWrapper is not iterable.")

    def __contains__(self, perm):
        return self[perm]


def perm(request):
    if hasattr(request, 'project'):
        project = request.project
    else:
        project = None
    wrapper = PermWrapper(request.user, project)
    return {'perm': wrapper}
