from django.utils.safestring import mark_safe
from django.db.models import Q
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

import bleach
from markdown import markdown

import hashlib

from tracker.models import Project
from tracker.mdx.mdx_issue import IssueExtension
from permissions.models import GlobalPermission
from permissions.models import PermissionModel as PermModel


from .issue_manager import IssueManager


__all__ = ['granted_project', 'markdown_to_html', 'get_message_id'
           'get_reply_addr', 'hexdigest_sha256', 'IssueFilter']


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


def markdown_to_html(value, project=None):
    # set extensions here if needed
    if project:
        base_url = settings.BASE_URL \
                + reverse('list-issue', args=[project.name]) + '{issue_id}/'
    else:
        base_url = '../{issue_id}/'
    mdx_issue = IssueExtension(base_url=base_url)
    value = markdown(value, extensions=[mdx_issue])
    value = bleach.clean(value, tags=bleach.ALLOWED_TAGS + ['p'])
    return mark_safe(value)


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
