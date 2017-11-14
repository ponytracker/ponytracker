from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from functools import wraps

from tracker.models import Project


def project_perm_required(perm):

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if 'project' in kwargs.keys():
                project = kwargs['project']
            else:
                project = None
            if request.user.has_perm(perm, project):
                return view(request, *args, **kwargs)
            elif request.user.is_authenticated:
                raise PermissionDenied()
            else:
                return login_required(view)(request, *args, **kwargs)
        return wrapper

    return decorator
