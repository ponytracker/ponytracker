from tracker.models import Project


def projects(request):

    c = {}

    if hasattr(request, 'archived'):
        c['archived'] = request.archived
    if hasattr(request, 'projects'):
        c['projects'] = request.projects

    return c
