from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django.http import Http404, HttpResponse, JsonResponse

from permissions.decorators import project_perm_required

from accounts.models import *
from accounts.forms import *


###########
# Profile #
###########

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


#########
# Users #
#########

@project_perm_required('manage_accounts')
def user_list(request):
    return render(request, 'accounts/user_list.html', {
        'users': User.objects.all(),
    })


@project_perm_required('manage_accounts')
def user_details(request, user):
    tab = request.session.pop('user-tab', 'group')
    return render(request, 'accounts/user_details.html', {
        'user': get_object_or_404(User, id=user),
        'directteams': Team.objects.filter(users__id=user),
        'tab': tab,
    })


@project_perm_required('manage_accounts')
def user_edit(request, user=None):

    if user:
        user = get_object_or_404(User, id=user)

    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            messages.success(request, 'User modified successfully.')
        else:
            messages.success(request, 'User added successfully.')
        return redirect('show-user', user.id)

    return render(request, 'accounts/user_edit.html', {
        'user': user,
        'form': form,
    })


@project_perm_required('manage_accounts')
def user_activate(request, user):
    user = get_object_or_404(User, id=user)
    if user.is_active:
        messages.info(request, 'Account already activated.')
    else:
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully.')
    return redirect('show-user', user.id)


@project_perm_required('manage_accounts')
def user_disable(request, user):
    user = get_object_or_404(User, id=user)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request, 'Account disabled successfully.')
    else:
        messages.info(request, 'Account already disabled.')
    return redirect('show-user', user.id)


@require_http_methods(["POST"])
@project_perm_required('manage_accounts')
def user_delete(request, user):
    user = get_object_or_404(User, id=user)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('list-user')


@project_perm_required('manage_accounts')
def user_add_group(request, user):
    user = get_object_or_404(User, id=user)
    if request.method == 'POST':
        group = request.POST.get('group')
        if group:
            try:
                group = Group.objects.get(name=group)
            except ObjectDoesNotExist:
                messages.error(request, 'Group not found.')
            else:
                if user.groups.filter(id=group.id).exists():
                    messages.info(request, 'User already in group.')
                else:
                    user.groups.add(group)
                    user.save()
                    messages.success(request,
                            'User added to group successfully.')
        else:
            messages.error(request, 'Group not found.')
        request.session['user-tab'] = 'group'
        return redirect('show-user', user.id)
    else:
        term = request.GET.get('term')
        if not term:
            return Http404()
        groups = Group.objects \
            .exclude(id__in=user.groups.values('id')) \
            .filter(name__icontains=term)[:10]
        response = []
        for group in groups:
            response += [{
                'label': group.name,
                'value': group.name,
            }]
        return JsonResponse(response, safe=False)


@project_perm_required('manage_accounts')
def user_remove_group(request, user, group):
    user = get_object_or_404(User, pk=user)
    group = get_object_or_404(Group, pk=group)
    user.groups.remove(group)
    user.save()
    return HttpResponse()


@project_perm_required('manage_accounts')
def user_add_team(request, user):
    user = get_object_or_404(User, id=user)
    if request.method == 'POST':
        team = request.POST.get('team')
        if team:
            try:
                team = Team.objects.get(name=team)
            except ObjectDoesNotExist:
                messages.error(request, 'Team not found.')
            else:
                # We do not use user.teams because we want to be able to add an
                # user to a team even if he is already a member through a group
                if Team.objects.filter(users=user).exists():
                    messages.info(request, 'User already in team.')
                else:
                    team.users.add(user)
                    team.save()
                    messages.success(request,
                            'User added to team successfully.')
        else:
            messages.error(request, 'Team not found.')
        request.session['user-tab'] = 'team'
        return redirect('show-user', user.id)
    else:
        term = request.GET.get('term')
        if not term:
            return Http404()
        teams = Team.objects \
            .exclude(users=user) \
            .filter(name__icontains=term)[:10]
        response = []
        for team in teams:
            response += [{
                'label': team.name,
                'value': team.name,
            }]
        return JsonResponse(response, safe=False)


@project_perm_required('manage_accounts')
def user_remove_team(request, user, team):
    user = get_object_or_404(User, pk=user)
    team = get_object_or_404(Team, pk=team)
    team.users.remove(user)
    team.save()
    response = ''
    if team.groups.filter(id__in=user.groups.values('id')).exists():
        # style a member throught a group
        response = '<em>member throught group</em>'
    return HttpResponse(response)


##########
# Groups #
##########

@project_perm_required('manage_accounts')
def group_list(request):
    return render(request, 'accounts/group_list.html', {
        'groups': Group.objects.all(),
    })


@project_perm_required('manage_accounts')
def group_details(request, group):
    return render(request, 'accounts/group_details.html', {
        'group': get_object_or_404(Group, id=group),
    })


@project_perm_required('manage_accounts')
def group_edit(request, group=None):

    if group:
        group = get_object_or_404(Group, id=group)

    form = GroupForm(request.POST or None, instance=group)
    if request.method == 'POST' and form.is_valid():
        formgroup = form.save()
        if group:
            messages.success(request, 'Group modified successfully.')
        else:
            messages.success(request, 'Group added successfully.')
        return redirect('show-group', formgroup.id)

    return render(request, 'accounts/group_edit.html', {
        'group': group,
        'form': form,
    })


@require_http_methods(["POST"])
@project_perm_required('manage_accounts')
def group_delete(request, group):
    group = get_object_or_404(Group, id=group)
    group.delete()
    messages.success(request, 'Group deleted successfully.')
    return redirect('list-group')


@project_perm_required('manage_accounts')
def group_add_user(request, group):
    group = get_object_or_404(Group, id=group)
    if request.method == 'POST':
        user = request.POST.get('user')
        if user:
            try:
                user = User.objects.get(username=user)
            except ObjectDoesNotExist:
                messages.error(request, 'User not found.')
            else:
                if group.users.filter(id=user.id).exists():
                    messages.info(request, 'User already in group.')
                else:
                    user.groups.add(group)
                    user.save()
                    messages.success(request,
                            'User added to group successfully.')
        else:
            messages.error(request, 'User not found.')
        return redirect('show-group', group.id)
    else:
        term = request.GET.get('term')
        if not term:
            return Http404()
        query = Q(username__icontains=term) \
            | Q(first_name__icontains=term) \
            | Q(last_name__icontains=term)
        users = User.objects.exclude(groups=group).filter(query)[:10]
        response = []
        for user in users:
            response += [{
                'label': user.username_and_fullname,
                'value': user.username,
            }]
        return JsonResponse(response, safe=False)


@project_perm_required('manage_accounts')
def group_remove_user(request, group, user):
    group = get_object_or_404(Group, id=group)
    user = get_object_or_404(User, id=user)
    user.groups.remove(group)
    user.save()
    return HttpResponse()


#########
# Teams #
#########

@project_perm_required('manage_accounts')
def team_list(request):
    return render(request, 'accounts/team_list.html', {
        'teams': Team.objects.all(),
    })


@project_perm_required('manage_accounts')
def team_details(request, team):
    tab = request.session.pop('team-tab', 'user')
    return render(request, 'accounts/team_details.html', {
        'team': get_object_or_404(Team, pk=team),
        'tab': tab,
    })


@project_perm_required('manage_accounts')
def team_edit(request, team=None):

    if team:
        team = get_object_or_404(Team, pk=team)

    form = TeamForm(request.POST or None, instance=team)
    if request.method == 'POST' and form.is_valid():
        formteam = form.save()
        if team:
            messages.success(request, 'Team modified successfully.')
        else:
            messages.success(request, 'Team added successfully.')
        return redirect('show-team', formteam.id)

    c = {
        'team': team,
        'form': form,
    }

    return render(request, 'accounts/team_edit.html', c)


@require_http_methods(["POST"])
@project_perm_required('manage_accounts')
def team_delete(request, team):
    team = get_object_or_404(Team, pk=team)
    team.delete()
    messages.success(request, 'Team deleted successfully.')
    return redirect('list-team')


@project_perm_required('manage_accounts')
def team_add_user(request, team):
    team = get_object_or_404(Team, id=team)
    if request.method == 'POST':
        user = request.POST.get('user')
        if user:
            try:
                user = User.objects.get(username=user)
            except ObjectDoesNotExist:
                messages.error(request, 'User not found.')
            else:
                if team.users.filter(id=user.id).exists():
                    messages.info(request, 'User already in team.')
                else:
                    team.users.add(user)
                    team.save()
                    messages.success(request,
                            'User added to team successfully.')
        else:
            messages.error(request, 'User not found.')
        request.session['team-tab'] = 'user'
        return redirect('show-team', team.id)
    else:
        term = request.GET.get('term')
        if not term:
            return Http404()
        query = Q(username__icontains=term) \
            | Q(first_name__icontains=term) \
            | Q(last_name__icontains=term)
        users = User.objects \
            .exclude(groups__in=team.groups.all()) \
            .exclude(id__in=team.users.values('id')) \
            .filter(query)[:10]
        response = []
        for user in users:
            response += [{
                'label': user.username_and_fullname,
                'value': user.username,
            }]
        return JsonResponse(response, safe=False)


@project_perm_required('manage_accounts')
def team_remove_user(request, team, user):
    team = get_object_or_404(Team, pk=team)
    user = get_object_or_404(User, pk=user)
    team.users.remove(user)
    team.save()
    return HttpResponse()


@project_perm_required('manage_accounts')
def team_add_group(request, team):
    team = get_object_or_404(Team, id=team)
    if request.method == 'POST':
        group = request.POST.get('group')
        if group:
            try:
                group = Group.objects.get(name=group)
            except ObjectDoesNotExist:
                messages.error(request, 'Group not found.')
            else:
                if team.groups.filter(id=group.id).exists():
                    messages.info(request, 'Group already in team.')
                else:
                    team.groups.add(group)
                    team.save()
                    messages.success(request,
                            'Group added to team successfully.')
        else:
            messages.error(request, 'Group not found.')
        request.session['team-tab'] = 'group'
        return redirect('show-team', team.id)
    else:
        term = request.GET.get('term')
        if not term:
            return Http404()
        groups = Group.objects \
            .exclude(id__in=team.groups.values('id')) \
            .filter(name__icontains=term)[:10]
        response = []
        for group in groups:
            response += [{
                'label': group.name,
                'value': group.name,
            }]
        return JsonResponse(response, safe=False)


@project_perm_required('manage_accounts')
def team_remove_group(request, team, group):
    team = get_object_or_404(Team, pk=team)
    group = get_object_or_404(Group, pk=group)
    team.groups.remove(group)
    team.save()
    return HttpResponse()
