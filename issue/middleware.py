from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from issue.models import *


class ProjectMiddleware:

    def process_view(self, request, view, view_args, view_kwargs):

        if view.__module__ != 'issue.views':
            return

        projects = Project.objects.filter(public=True)
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
