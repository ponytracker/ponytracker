from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from tracker.utils import granted_projects


# This middleware protect only views of the following modules
modules = ['accounts.views', 'permissions.views', 'tracker.views']


class ProjectMiddleware:
    """
    This middleware must be call after authentication middleware.
    """

    def process_view(self, request, view, view_args, view_kwargs):

        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The project middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the ProjectMiddleware class.")

        request.projects = granted_projects(request.user)

        # project
        if view.__module__ not in modules:
            return
        project = view_kwargs.get('project')
        if not project:
            return
        try:
            project = request.projects.get(name=project)
        except ObjectDoesNotExist:
            if request.user.is_authenticated():
                raise PermissionDenied()
            else:
                return login_required(view)(request, *view_args, **view_kwargs)
        view_kwargs['project'] = project
        request.project = project
