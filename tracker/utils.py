from django.utils.safestring import mark_safe
from django.db.models import Q

from markdown import markdown

from tracker.models import Project
from permissions.models import GlobalPermission
from permissions.models import PermissionModel as PermModel


def granted_projects(user):
    if user.is_authenticated() and user.is_staff:
        return Project.objects.all()
    elif user.is_authenticated():
        teams = user.teams.values_list('id')
        groups = user.groups.values_list('id')
        # check for a global permission allowing access
        if GlobalPermission.objects.filter(access_project=True) \
                .filter(
                    # directly
                    Q(grantee_type=PermModel.GRANTEE_USER,
                        grantee_id=user.id)
                    # through a group
                    | Q(grantee_type=PermModel.GRANTEE_GROUP,
                        grantee_id__in=groups)
                    # through a team
                    | Q(grantee_type=PermModel.GRANTEE_TEAM,
                        grantee_id__in=teams)
                ).exists():
            return Project.objects.all()
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
                    permissions__grantee_id=user.id)
            return Project.objects.filter(query).distinct()
    else:
        # only public projects
        return Project.objects.filter(access=Project.ACCESS_PUBLIC)

def markdown_to_html(value):
    # set extensions here if needed
    return mark_safe(markdown(value, safe_mode='escape'))
