from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from issue.models import Project


def project_perm_required(perm):

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if len(args) > 0 and isinstance(args[0], Project):
                project = args[0]
            elif 'project' in kwargs.keys():
                project = kwargs['project']
            else:
                project = None
            if request.user.has_perm(perm, project):
                return view(request, *args, **kwargs)
            elif request.user.is_authenticated():
                return HttpResponseForbidden()
            else:
                return login_required(view)(request, *args, **kwargs)
        return wrapper

    return decorator
