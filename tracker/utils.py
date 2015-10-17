from django.utils.safestring import mark_safe
from django.db.models import Q
from django.conf import settings
from django.contrib.sites.models import Site

import bleach
from markdown import markdown

import shlex
from sys import version_info as python_version
import hashlib

from tracker.models import Project
from tracker.mdx.mdx_issue import IssueExtension
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
    mdx_issue = IssueExtension(base_url='../{issue_id}/')
    value = bleach.clean(value)
    return mark_safe(markdown(value, extensions=[mdx_issue]))


def shell_split(cmd):

   if python_version < (3,):
       cmd = cmd.encode('utf-8')
   
   args = shlex.split(cmd)
   
   if python_version < (3,):
       args = [ arg.decode('utf-8') for arg in args ]

   return args


def get_message_id(mid):

    from_email = settings.DEFAULT_FROM_EMAIL

    return '<%s.%s.%s>' % (mid, hexdigest_sha256(mid, from_email), from_email)


def get_reply_addr(mid, dest):

    if not hasattr(settings, 'REPLY_EMAIL'):
        return []

    addr = settings.REPLY_EMAIL
    pos = addr.find('@')
    name = addr[:pos]
    domain = addr[pos:]
    token = hexdigest_sha256(settings.SECRET_KEY, mid, dest.pk)

    return ['%s+%s.%d.%s%s' % (name, mid, dest.pk, token, domain)]


def hexdigest_sha256(*args):

    r = hashlib.sha256()
    for arg in args:
        r.update(str(arg).encode('utf-8'))

    return r.hexdigest()
