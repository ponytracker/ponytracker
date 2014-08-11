from django.contrib.auth.views import redirect_to_login


def permission_granted_or_login(request, perm):

    if hasattr(request, 'project'):
        project = request.project
    else:
        project = None
    if not request.user.has_perm(perm, project):
        return redirect_to_login(request.build_absolute_uri())
