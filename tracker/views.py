from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.db.models import Max

from tracker.utils import markdown_to_html
from tracker.forms import *
from tracker.models import *
from tracker.notifications import *
from accounts.models import User
from permissions.models import ProjectPermission
from permissions.decorators import project_perm_required

import shlex
from collections import OrderedDict


STATUS_VALUES = OrderedDict([
        ('is:open', 'Open'),
        ('is:close', 'Closed'),
        ('*', 'All'),
    ])
SORT_VALUES = OrderedDict([
        ('recently-updated', 'Recentely updated'),
        ('least-recently-updated', 'Least recently updated'),
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
#        ('most-commented', 'Most commented'),
#        ('least-commented', 'Least commented'),
    ])


####################
# Markdown preview #
####################

@login_required
@require_http_methods(["POST"])
def markdown_preview(request):
    content = request.POST.get('data', '')
    return HttpResponse(markdown_to_html(content))


#########
# Admin #
#########

@login_required
def admin(request):
    if request.user.has_perm('manage_settings'):
        return redirect('settings')
    elif request.user.has_perm('manage_accounts'):
        return redirect('list-user')
    elif request.user.has_perm('manage_global_permission'):
        return redirect('list-global-permission')
    else:
        raise PermissionDenied()


############
# Settings #
############

@project_perm_required('manage_settings')
def settings_list(request):

    form = SettingsForm(request.POST or None, instance=get_current_site(request).settings)

    if request.method == 'POST' and form.is_valid():

        form.save()
        messages.success(request, 'Settings successfully updated.')

        return redirect('settings')

    c = {
        'form': form,
    }

    return render(request, 'tracker/settings.html', c)


############
# Projects #
############

def project_list(request):

    if not request.projects.exists():

        if request.user.has_perm('create_project'):
            messages.info(request, 'Start by creating a project.')
            return redirect('add-project')

    return render(request, 'tracker/project_list.html')


def project_redirect(request, project):

    return redirect('list-issue', project.name)


@project_perm_required('create_project')
def project_add(request):

    form = ProjectForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        name = form.cleaned_data['name']
        display_name = form.cleaned_data['display_name']
        if name in settings.RESERVED_PROJECT_URLS:
            form._errors['name'] = ['Sorry, this URL is reserved '
                                    'and can not be used.']
        elif Project.objects.filter(display_name__iexact=display_name).exists():
            form._errors['display_name'] = ['There is already a project '
                                            'with a similar name.']
        else:
            project = form.save()
            messages.success(request, 'Project added successfully.')
            project.subscribers.add(request.user)
            ProjectPermission.objects.create(project=project,
                    manage_project_permission=True,
                    grantee=request.user)
            return redirect('list-project-permission', project.name)

    c = {
        'form': form,
    }

    return render(request, 'tracker/project_add.html', c)


@project_perm_required('modify_project')
def project_edit(request, project):

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == 'POST' and form.is_valid():

        name = form.cleaned_data['name']
        display_name = form.cleaned_data['display_name']
        if name in settings.RESERVED_PROJECT_URLS:
            form._errors['name'] = ['Sorry, this URL is reserved '
                                    'and can not be used.']
        elif Project.objects.filter(display_name__iexact=display_name) \
                .exclude(pk=project.pk).exists():
            form._errors['display_name'] = ['There is already a project '
                                            'with a similar name.']
        else:
            project = form.save()
            messages.success(request, 'Project modified successfully.')
            return redirect('list-issue', project.name)

    c = {
        'project': project,
        'form': form,
    }

    return render(request, 'tracker/project_edit.html', c)


@require_http_methods(["POST"])
@project_perm_required('delete_project')
def project_delete(request, project):

    project.delete()

    messages.success(request, 'Project deleted successfully.')

    return redirect('list-project')


@login_required
def project_subscribe(request, project):

    if not request.user.email:
        messages.error(request, 'You must set an email address in your '
            '<a href="' + reverse('profile') + '">profile</a> in order '
            'to watch this project.')
    elif request.user.notifications == User.NOTIFICATIONS_NEVER:
        messages.error(request, 'You must enable notifications in your '
            '<a href="' + reverse('profile') + '">profile</a> in order '
            'to watch this project.')
    elif project.subscribers.filter(pk=request.user.pk).exists():
        messages.warning(request,
                'You are already subscribed to this project.')
    else:
        project.subscribers.add(request.user)
        project.save()
        messages.success(request,
                'You have been subscribed to this project successfully.')

    next = request.GET.get('next')
    if next:
        return redirect(next)
    else:
        return redirect('list-issue', project.name)


@login_required
def project_unsubscribe(request, project):

    if project.subscribers.filter(pk=request.user.pk).exists():
        project.subscribers.remove(request.user)
        project.save()
        messages.success(request, 'You will not receive any notifications '
                                  'for this project anymore.')
    else:
        messages.warning(request, 'You are not subscribed to this project.')

    next = request.GET.get('next')
    if next:
        return redirect(next)
    else:
        return redirect('list-issue', project.name)


##########
# Issues #
##########

def issue_list(request, project):

    issues = project.issues

    labels = Label.objects.filter(project=project)
    milestones = Milestone.objects.filter(project=project)

    sort = request.GET.get('sort', '')
    sort_default_behaviour = 'recently-updated'
    if sort == '' or sort not in SORT_VALUES.keys():
        sort = sort_default_behaviour

    status = None

    query = request.GET.get('q', '')
    query_without_status = ''

    syntaxe_error = False
    for constraint in shlex.split(query):

        if constraint == '*':
            status = '*'
            continue

        args = constraint.split(':')

        if len(args) != 2:
            messages.error(request, 'There is a syntaxe error in your filter.')
            issues = None
            break

        key = args[0]
        value = args[1]

        if key == '':
            continue

        elif key == 'is':
            if status:
                messages.error(request, "The keyword 'is' can appear only "
                                        "one time.")
                issues = None
                break
            elif value == 'open':
                issues = issues.filter(closed=False)
                status = 'is:open'
            elif value == 'close':
                issues = issues.filter(closed=True)
                status = 'is:close'
            else:
                messages.error(request, "The keyword 'is' must be followed "
                                        "by 'open' or 'close'.")
                issues = None
                break

        elif key == 'label':
            try:
                label = Label.objects.get(project=project,
                        name=value, deleted=False)
            except ObjectDoesNotExist:
                messages.error(request, "The label '%s' does not exist "
                                        "or has been deleted." % value)
                issues = None
                break
            else:
                issues = issues.filter(labels=label)
                labels = labels.exclude(pk=label.pk)

        elif key == 'milestone':
            try:
                milestone = Milestone.objects.get(project=project, name=value)
            except ObjectDoesNotExist:
                messages.error(request, "The milestone '%s' does not exist."
                        % value)
                issues = None
                break
            else:
                issues = issues.filter(milestone=milestone)
                milestones = milestones.exclude(pk=milestone.pk)

        elif key == 'due':
            if value == 'yes':
                issues = issues.filter(due_date__isnull=False)
            elif value == 'no':
                issues = issues.filter(due_date__isnull=True)
            else:
                messages.error(request, "The keyword 'due' must be followed "
                                        "by 'yes' or 'no'.")
                issues = None
                break

        elif key == 'author' or key == 'user':
            if User.objects.filter(username=value).exists():
                issues = issues.filter(author__username=value)
            else:
                messages.error(request, "The user '%s' does not exist."
                        % value)
                issues = None
                break

        else:
            messages.error(request, "Unknow '%s' filtering criterion." % key)
            issues = None
            break

        if key != 'is':
            query_without_status += ' ' + constraint

    if issues:
        if not status:
            issues = issues.filter(closed=False)
        if sort == 'newest':
            issues = issues.order_by('-opened_at')
        elif sort == 'oldest':
            issues = issues.order_by('opened_at')
        elif sort == 'least-recently-updated':
            issues = issues.annotate(last_activity=Max('events__date')).order_by('last_activity')
        else: # recently-updated
            issues = issues.annotate(last_activity=Max('events__date')).order_by('-last_activity')
        page = request.GET.get('page')
        paginator = Paginator(issues,
                get_current_site(request).settings.items_per_page)
        try:
            issues = paginator.page(page)
        except PageNotAnInteger:
            issues = paginator.page(1)
        except EmptyPage:
            issues = paginator.page(paginator.num_pages)
    else:
        paginator = None

    if not status:
        status = 'is:open'
    if not query:
        query = status
    if sort != sort_default_behaviour:
        sort_url = '&sort=' + sort
    else:
        sort_url = ''

    c = {
        'project': project,
        'issues': issues,
        'labels': labels,
        'milestones': milestones,
        'paginator': paginator,
        'status': status, # for active status tab
        'status_values': STATUS_VALUES,
        'query': query_without_status, # to generate url with other status
        'full_query': query, # for query field
        'sort': sort,
        'sort_url': sort_url,
        'sort_values': SORT_VALUES,
    }

    return render(request, 'tracker/issue_list.html', c)


@login_required
def issue_edit(request, project, issue=None):

    if issue:
        if not request.user.has_perm('modify_issue', project):
            raise PermissionDenied()
        issue = get_object_or_404(Issue, project=project, id=issue)
        init_data = {'title': issue.title,
                     'due_date': issue.due_date,
                     'description': issue.description}
    else:
        if not request.user.has_perm('create_issue', project):
            raise PermissionDenied()
        issue = None
        init_data = None

    form = IssueForm(request.POST or init_data)

    if request.method == 'POST' and form.is_valid():

        title = form.cleaned_data['title']
        due_date = form.cleaned_data['due_date']
        description = form.cleaned_data['description']

        if issue:

            modified = False

            if issue.title != title:
                old_title = issue.title
                event = Event(issue=issue, author=request.user,
                        code=Event.RENAME,
                        args={'old_title': old_title, 'new_title': title})
                event.save()
                issue.title = title
                modified = True

            if issue.due_date != due_date:
                # TODO: create new event 'due date changed'
                issue.due_date = due_date
                modified = True

            if issue.description != description:
                issue.description = description
                modified = True

            if modified:
                issue.save()
                messages.success(request, 'Issue updated successfully.')
            else:
                messages.info(request, 'Issue not modified.')

        else:

            issue = Issue(title=title, due_date=due_date, author=request.user,
                    project=project, id=Issue.next_id(project))
            issue.save()
            issue.subscribers.add(request.user)
            issue.description = description
            notify_new_issue(issue)
            messages.success(request, 'Issue created successfully.')

        return redirect('show-issue', project.name, issue.id)

    c = {
        'project': project,
        'form': form,
        'issue': issue,
    }

    return render(request, 'tracker/issue_edit.html', c)


def issue_details(request, project, issue):

    issue = get_object_or_404(Issue, project=project, id=issue)

    labels = Label.objects.filter(project=project, deleted=False) \
        .exclude(id__in=issue.labels.all().values_list('id'))
    milestones = Milestone.objects.filter(project=project)
    if issue.milestone:
        milestones = milestones.exclude(name=issue.milestone.name)

    events = issue.events.all()

    if request.user.has_perm('create_comment', project):
        form = CommentForm(request.POST or None)
    else:
        form = None

    c = {
        'labels': labels,
        'milestones': milestones,
        'project': project,
        'issue': issue,
        'events': events,
        'form': form,
    }

    return render(request, 'tracker/issue_details.html', c)


@login_required
def issue_comment_edit(request, project, issue, comment=None):

    issue = get_object_or_404(Issue, project=project, id=issue)

    change_state = False
    if 'change-state' in request.POST:
        if not request.user.has_perm('manage_issue', project):
            raise PermissionDenied()
        change_state = True

    if comment:
        if not request.user.has_perm('modify_comment', project):
            raise PermissionDenied()
        event = get_object_or_404(Event, code=Event.COMMENT,
                issue=issue, id=comment)
        init_data = {'comment': event.additionnal_section}
    else:
        if not request.user.has_perm('create_comment', project):
            raise PermissionDenied()
        event = None
        init_data = None

    form = CommentForm(request.POST or init_data)

    if request.method == 'POST' and form.is_valid():

        redirect_to = 'issue'
        comment = form.cleaned_data['comment']

        # modification of an existent comment
        if event:

            if event.additionnal_section != comment:
                event.additionnal_section = comment
                event.save()
                messages.success(request, 'Comment modified successfully.')
            else:
                messages.info(request, 'Comment not modified.')

        # creation of a new comment
        else:

            event = Event(issue=issue, author=request.user,
                    code=Event.COMMENT, additionnal_section=comment)
            event.save()
            issue.subscribers.add(request.user)
            notify_new_comment(event)
            if change_state:
                issue.closed = not issue.closed
                issue.save()
                if issue.closed:
                    event = Event(issue=issue, author=request.user, code=Event.CLOSE)
                    event.save()
                    notify_close_issue(event)
                    messages.success(request, 'Comment added successfully and issue closed.')
                    redirect_to = 'list'
                else:
                    event = Event(issue=issue, author=request.user, code=Event.REOPEN)
                    event.save()
                    notify_reopen_issue(event)
                    messages.success(request, 'Issue reopened and omment added successfully.')
            else:
                messages.success(request, 'Comment added successfully.')

        if redirect_to == 'issue':
            return redirect('show-issue', project.name, issue.id)
        else:
            return redirect('list-issue', project.name)

    c = {
        'project': project,
        'issue': issue,
        'comment': event,
        'form': form,
    }

    return render(request, 'tracker/comment_edit.html', c)


@require_http_methods(["POST"])
@project_perm_required('delete_comment')
def issue_comment_delete(request, project, issue, comment):

    comment = get_object_or_404(Event,
            issue__project=project, issue__id=issue, id=comment)

    comment.delete()
    messages.success(request, 'Comment deleted successfully.')

    return redirect('show-issue', project.name, issue)


@project_perm_required('manage_issue')
def issue_close(request, project, issue):

    issue = get_object_or_404(Issue, project=project, id=issue, closed=False)

    issue.closed = True
    issue.save()

    event = Event(issue=issue, author=request.user, code=Event.CLOSE)
    event.save()

    notify_close_issue(event)

    messages.success(request, 'Issue closed.')

    return redirect('list-issue', project.name)


@project_perm_required('manage_issue')
def issue_reopen(request, project, issue):

    issue = get_object_or_404(Issue, project=project, id=issue, closed=True)

    issue.closed = False
    issue.save()

    event = Event(issue=issue, author=request.user, code=Event.REOPEN)
    event.save()

    notify_reopen_issue(event)

    messages.success(request, 'Issue reopened.')

    return redirect('show-issue', project.name, issue.id)


@require_http_methods(["POST"])
@project_perm_required('delete_issue')
def issue_delete(request, project, issue):

    issue = get_object_or_404(Issue, project=project, id=issue)

    issue.delete()

    messages.success(request, 'Issue deleted successfully.')

    return redirect('list-issue', project.name)


@project_perm_required('manage_tags')
def issue_add_label(request, project, issue, label):

    issue = get_object_or_404(Issue, project=project, id=issue)
    label = get_object_or_404(Label, project=project, id=label)

    issue.add_label(request.user, label)

    return redirect('show-issue', project.name, issue.id)


@project_perm_required('manage_tags')
def issue_remove_label(request, project, issue, label):

    issue = get_object_or_404(Issue, project=project, id=issue)
    label = get_object_or_404(Label, project=project, id=label)

    issue.remove_label(request.user, label)

    return redirect('show-issue', project.name, issue.id)


@project_perm_required('manage_tags')
def issue_add_milestone(request, project, issue, milestone):

    issue = get_object_or_404(Issue, project=project, id=issue)
    milestone = get_object_or_404(Milestone, project=project, name=milestone)

    issue.add_milestone(request.user, milestone)

    return redirect('show-issue', project.name, issue.id)


@project_perm_required('manage_tags')
def issue_remove_milestone(request, project, issue, milestone):

    issue = get_object_or_404(Issue, project=project, id=issue)
    milestone = get_object_or_404(Milestone, project=project, name=milestone)

    issue.remove_milestone(request.user, milestone)

    return redirect('show-issue', project.name, issue.id)


@login_required
def issue_subscribe(request, project, issue):

    issue = get_object_or_404(Issue, project=project, id=issue)

    if not request.user.email:
        messages.error(request, 'You must set an email address in your '
            '<a href="' + reverse('profile') + '">profile</a> to subscribe.')
    elif request.user.notifications == User.NOTIFICATIONS_NEVER:
        messages.error(request, 'You must enable notifications in your '
            '<a href="' + reverse('profile') + '">profile</a> to subscribe.')
    elif issue.subscribers.filter(pk=request.user.pk).exists():
        messages.warning(request, 'You are already subscribed to this issue.')
    else:
        issue.subscribers.add(request.user)
        issue.save()
        messages.success(request,
                'You have been subscribed to this issue successfully.')

    return redirect('show-issue', project.name, issue.id)


@login_required
def issue_unsubscribe(request, project, issue):

    issue = get_object_or_404(Issue, project=project, id=issue)

    if issue.subscribers.filter(pk=request.user.pk).exists():
        issue.subscribers.remove(request.user)
        issue.save()
        messages.success(request, 'You will not receive any notifications '
                                  'for this issue anymore.')
    else:
        messages.warning(request, 'You are not subscribed to this issue.')

    return redirect('show-issue', project.name, issue.id)


##########
# Labels #
##########

def label_list(request, project):

    labels = project.labels.filter(deleted=False)

    return render(request, 'tracker/label_list.html', {
        'project': project,
        'labels': labels,
    })


@project_perm_required('manage_tags')
def label_edit(request, project, id=None):

    if id:
        label = get_object_or_404(Label, project=project, id=id)
    else:
        label = None
    issue = request.GET.get('issue')
    if issue:
        issue = get_object_or_404(Issue, project=project, id=issue)

    form = LabelForm(request.POST or None, instance=label)

    if request.method == 'POST' and form.is_valid():

        similar = Label.objects.filter(project=project,
                name=form.cleaned_data['name'], deleted=False)

        if label:
            similar = similar.exclude(pk=label.pk)

        if similar.exists():

            form._errors['name'] = ['There is already a label with this name.']

        else:

            if label:
                form.save()
                messages.success(request, 'Label modified successfully.')
            else:
                label = form.save(commit=False)
                label.project = project
                label.save()
                messages.success(request, 'Label added successfully.')

            if issue:
                return redirect('add-label-to-issue',
                        project.name, issue.id, label.id)

            return redirect('list-label', project.name)

    if issue:
        cancel = reverse('show-issue', args=[project.name, issue.id])
    else:
        cancel = reverse('list-label', args=[project.name])

    c = {
        'project': project,
        'form': form,
        'label': label,
        'cancel': cancel,
    }

    return render(request, 'tracker/label_edit.html', c)


@require_http_methods(["POST"])
@project_perm_required('delete_tags')
def label_delete(request, project, id):

    label = get_object_or_404(Label, project=project, id=id)

    for issue in label.issues.all():
        issue.remove_label(request.user, label)
    label.deleted = True
    label.save()

    messages.success(request, "Label deleted successfully.")

    return redirect('list-label', project.name)


##############
# Milestones #
##############

def milestone_list(request, project):

    show = request.GET.get('show', 'open')

    if show == 'open':
        milestones = project.milestones.filter(closed=False)
    elif show == 'close':
        milestones = project.milestones.filter(closed=True)
    elif show == 'all':
        milestones = project.milestones.all()
    else:
        messages.error(request, 'There is an error in your filter.')
        milestones = None

    return render(request, 'tracker/milestone_list.html', {
        'project': project,
        'milestones': milestones,
        'show': show,
    })


@project_perm_required('manage_tags')
def milestone_edit(request, project, name=None):

    if name:
        milestone = get_object_or_404(Milestone, project=project, name=name)
    else:
        milestone = None
    issue = request.GET.get('issue')
    if issue:
        issue = get_object_or_404(Issue, project=project, id=issue)

    form = MilestoneForm(request.POST or None, instance=milestone)

    if request.method == 'POST' and form.is_valid():

        similar = Milestone.objects.filter(project=project,
                name=form.cleaned_data['name'])

        if milestone:
            similar = similar.exclude(pk=milestone.pk)

        if similar.exists():

            form._errors['name'] = ['There is already a milestone '
                                    'with this name.']

        else:

            if milestone:
                if name != form.cleaned_data['name']:
                    for i in milestone.issues.all():
                        event = Event(issue=i, author=request.user,
                                code=Event.CHANGE_MILESTONE, args={
                                    'old_milestone': name,
                                    'new_milestone': form.cleaned_data['name']
                                })
                        event.save()
                form.save()
                messages.success(request, 'Milestone modified successfully.')
            else:
                milestone = form.save(commit=False)
                milestone.project = project
                milestone.save()
                messages.success(request, 'Milestone added successfully.')

            if issue:
                return redirect('add-milestone-to-issue',
                        project.name, issue.id, milestone.name)

            return redirect('list-milestone', project.name)

    if issue:
        cancel = reverse('show-issue', args=[project.name, issue.id])
    else:
        cancel = reverse('list-milestone', args=[project.name])

    c = {
        'project': project,
        'form': form,
        'milestone': milestone,
        'cancel': cancel,
    }

    return render(request, 'tracker/milestone_edit.html', c)


@project_perm_required('manage_tags')
def milestone_close(request, project, name):

    milestone = get_object_or_404(Milestone, closed=False, project=project, name=name)

    milestone.closed = True
    milestone.save()

    return redirect('list-milestone', project.name)


@project_perm_required('manage_tags')
def milestone_reopen(request, project, name):

    milestone = get_object_or_404(Milestone, closed=True, project=project, name=name)

    milestone.closed = False
    milestone.save()

    return redirect('list-milestone', project.name)


@require_http_methods(["POST"])
@project_perm_required('delete_tags')
def milestone_delete(request, project, name):

    milestone = get_object_or_404(Milestone, project=project, name=name)

    for issue in milestone.issues.all():
        issue.remove_milestone(request.user, milestone)
    milestone.delete()

    messages.success(request, "Label deleted successfully.")

    return redirect('list-milestone', project.name)
