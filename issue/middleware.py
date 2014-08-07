from issue.models import *


class ProjectMiddleware:

    def process_view(self, request, view, view_args, view_kwargs):

        if view.__module__ != 'issue.views':
            return

        projects = Project.objects.all()
        request.projects = projects
