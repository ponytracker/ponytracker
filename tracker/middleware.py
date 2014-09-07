from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from tracker.models import Project
from permissions.models import GlobalPermission
from permissions.models import PermissionModel as PermModel


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

        # projectS
        if request.user.is_authenticated() and request.user.is_staff:
            projects = Project.objects.all()
        elif request.user.is_authenticated():
            teams = request.user.teams.values_list('id')
            groups = request.user.groups.values_list('id')
            # check for a global permission allowing access
            if GlobalPermission.objects.filter(access_project=True) \
                    .filter(
                        # directly
                        Q(grantee_type=PermModel.GRANTEE_USER,
                            grantee_id=request.user.id)
                        # through a group
                        | Q(grantee_type=PermModel.GRANTEE_GROUP,
                            grantee_id__in=groups)
                        # through a team
                        | Q(grantee_type=PermModel.GRANTEE_TEAM,
                            grantee_id__in=teams)
                    ).exists():
                projects = Project.objects.all()
            # searching project reachable throught project permission
            else:
                # public project
                query = Q(access=Project.ACCESS_PUBLIC)
                # project reserved to logged users
                query |= Q(access=Project.ACCESS_REGISTERED)
                # access granted through a team
                query |= Q(permissions__grantee_type=PermModel.GRANTEE_TEAM,
                        permissions__grantee_id__in=teams)
                # access granted through a group
                query |= Q(permissions__grantee_type=PermModel.GRANTEE_GROUP,
                        permissions__grantee_id__in=groups)
                # access granted by specific permission
                query |= Q(permissions__grantee_type=PermModel.GRANTEE_USER,
                        permissions__grantee_id=request.user.id)
                projects = Project.objects.filter(query).distinct()
        else:
            # only public projects
            projects = Project.objects.filter(access=Project.ACCESS_PUBLIC)
        request.projects = projects

        # project
        if view.__module__ not in modules:
            return
        project = view_kwargs.get('project')
        if not project:
            return
        try:
            project = projects.get(name=project)
        except ObjectDoesNotExist:
            if request.user.is_authenticated():
                raise PermissionDenied()
            else:
                return login_required(view)(request, *view_args, **view_kwargs)
        view_kwargs['project'] = project
        request.project = project
