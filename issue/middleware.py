from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from issue.models import *


class ProjectMiddleware:
    """
    This middleware must be call after authentication middleware.
    """

    def process_view(self, request, view, view_args, view_kwargs):

        if view.__module__ != 'issue.views':
            return

        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The project middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the ProjectMiddleware class.")

        user = None
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user)

        query = Q(public=True)
        if user:
            # access granted through a team
            query |= Q(permissions__grantee_type=PermissionModel.GRANTEE_TEAM,
                    permissions__grantee_name__in=user.teams.values_list('name'))
            # access granted through a group
            query |= Q(permissions__grantee_type=PermissionModel.GRANTEE_GROUP,
                    permissions__grantee_name__in=user.groups.values_list('name'))
            # access granted by specific permission
            query |= Q(permissions__grantee_type=PermissionModel.GRANTEE_USER,
                    permissions__grantee_name=user.username)
        projects = Project.objects.filter(query)
        request.projects = projects

        project = view_kwargs.get('project')
        if not project:
            return
        try:
            project = projects.get(name=project)
        except ObjectDoesNotExist:
            if request.user.is_authenticated():
                return HttpResponseForbidden()
            else:
                return login_required(view)(request, *view_args, **view_kwargs)
        view_kwargs['project'] = project
