from tracker.models import Project


def projects(request):

    if hasattr(request, 'projects'):
        return {'projects': request.projects}
    else:
        return {}
