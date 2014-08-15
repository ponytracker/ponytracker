from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.core.urlresolvers import reverse

from issue.models import Project


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
            elif request.user.is_authenticated():
                return HttpResponseForbidden()
            else:
                return login_required(view)(request, *args, **kwargs)
        return wrapper

    return decorator

def confirmation_required(message, previous=None):

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.GET.get('force'):
                return view(request, *args, **kwargs)
            prev = previous
            if not prev:
                prev = request.GET.get('prev')
                if not prev:
                    # improvising
                    if hasattr(request, 'project'):
                        prev = reverse('list-issue',
                            args=[request.project.name])
                    else:
                        prev = reverse('list-project')
            c = {
                'message': message,
                'prev': prev,
                'next': request.path + '?force=1',
            }
            return render(request, 'confirm.html', c)
        return wrapper

    return decorator
