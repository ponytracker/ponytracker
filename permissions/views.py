from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied


from permissions.models import *
from permissions.forms import *
from permissions.decorators import project_perm_required


@project_perm_required('manage_global_permission')
def global_perm_list(request):
    return render(request, 'permissions/global_perm_list.html', {
        'permissions': GlobalPermission.objects.all(),
    })


@project_perm_required('manage_global_permission')
def global_perm_edit(request, id=None):
    if id:
        perm = get_object_or_404(GlobalPermission, id=id)
    else:
        perm = None
    form = GlobalPermissionForm(request.POST or None, instance=perm)
    if request.method == 'POST' and form.is_valid():
        form.save()
        if id:
            messages.success(request, 'Permission updated successfully.')
        else:
            messages.success(request, 'Permission added successfully.')
        return redirect('list-global-permission')
    name = request.POST.get('grantee_name')
    if not name:
        if perm:
            name = perm.grantee.__str__()
        else:
            name = ''
    return render(request, 'permissions/global_perm_edit.html', {
        'permission': perm,
        'form': form,
        'name': name,
    })


@require_http_methods(["POST"])
@project_perm_required('manage_global_permission')
def global_perm_delete(request, id):
    perm = get_object_or_404(GlobalPermission, id=id)
    perm.delete()
    messages.success(request, 'Permission deleted successfully.')
    return redirect('list-global-permission')


@project_perm_required('manage_global_permission')
def global_perm_toggle(request, id, perm):
    permission = get_object_or_404(GlobalPermission, id=id)
    # to be sure to dont modify other attribut with the following trick
    if '-' not in perm:
        raise Http404
    perm = perm.replace('-', '_')
    if hasattr(permission, perm):
        state = not getattr(permission, perm)
        setattr(permission, perm, state)
        permission.save()
        return HttpResponse('1' if state else '0')
    else:
        raise Http404


@project_perm_required('manage_project_permission')
def project_perm_list(request, project):
    return render(request, 'permissions/project_perm_list.html', {
        'project': project,
        'permissions': ProjectPermission.objects.filter(project=project).all(),
    })


@project_perm_required('manage_project_permission')
def project_perm_edit(request, project, id=None):
    if id:
        perm = get_object_or_404(ProjectPermission, project=project, id=id)
    else:
        perm = None
    form = ProjectPermissionForm(request.POST or None, instance=perm,
            initial={'project': project.id})
    if request.method == 'POST' and form.is_valid():
        if not form.cleaned_data['project'] == project:
            raise PermissionDenied()
        form.save()
        if id:
            messages.success(request, 'Permission updated successfully.')
        else:
            messages.success(request, 'Permission added successfully.')
        return redirect('list-project-permission', project.name)
    name = request.POST.get('grantee_name')
    if not name:
        if perm:
            name = perm.grantee.__str__()
        else:
            name = ''
    return render(request, 'permissions/project_perm_edit.html', {
        'project': project,
        'permission': perm,
        'form': form,
        'name': name,
    })


@project_perm_required('manage_project_permission')
def project_perm_delete(request, project, id):
    perm = get_object_or_404(ProjectPermission, project=project, id=id)
    perm.delete()
    messages.success(request, 'Permission deleted successfully.')
    return redirect('list-project-permission', project.name)


@project_perm_required('manage_project_permission')
def project_perm_toggle(request, project, id, perm):
    permission = get_object_or_404(ProjectPermission, project=project, id=id)
    # to be sure to dont modify other attribut with the following trick
    if '-' not in perm:
        raise Http404
    perm = perm.replace('-', '_')
    if hasattr(permission, perm):
        state = not getattr(permission, perm)
        setattr(permission, perm, state)
        permission.save()
        return HttpResponse('1' if state else '0')
    else:
        raise Http404
