from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.forms.models import modelform_factory
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from issue.models import *

from django_markdown.widgets import MarkdownWidget


def project_list(request):

    projects = Project.objects.all()

    if not projects.count():

        messages.info(request, 'Start by creating a project.')

        return redirect('add-project')

    c = {
            'request': request,
            'projects': projects,
        }

    return render(request, 'issue/project_list.html', c)

def project_edit(request, project=None):

    if project:
        project = get_object_or_404(Project, name=project)

    class ProjectForm(forms.ModelForm):

        class Meta:
            model=Project
            fields=['display_name', 'name', 'description']

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == 'POST' and form.is_valid():

        project = form.save()
        messages.success(request, 'Project added successfully.')

        return redirect('list-issue', project.name)

    projects = Project.objects.all()

    c = {
            'request': request,
            'projects': projects,
            'project': project,
            'form': form,
        }

    return render(request, 'issue/project_edit.html', c)

def project_delete(request, project):

    project = get_object_or_404(Project, name=project)

    project.delete()

    messages.success(request, 'Project deleted successfully.')

    return redirect('list-project')

def issue_list(request, project):

    project = get_object_or_404(Project, name=project)

    projects = Project.objects.all()

    issues = project.issues

    query = request.GET.get('q', 'open')

    constraints = query.split(' ')

    error = False
    for constraint in constraints:

        if constraint == 'open':
            issues = issues.filter(closed=False)
        elif constraint == 'close':
            issues = issues.filter(closed=True)
        elif constraint == 'all':
            pass
        else:
            args = constraint.split(':')
            if len(args) != 2:
                error = True
                break
            if len(args) == 2 and args[0] == 'label':
                try:
                    label = Label.objects.get(name=args[1])
                except ObjectDoesNotExist:
                    messages.info(request, "The label '%s' does not exist"
                                        ", ignoring the constraint." %args[1])
                else:
                    issues = issues.filter(labels=label)
            else:
                error = True
                break

    if error:
        messages.error(request, 'There is a syntaxe error in your filter.')
        issues = project.issues.filter(closed=False)

    issues = issues.extra(order_by=['-opened_at'])

    c = {
            'request': request,
            'projects': projects,
            'project': project,
            'issues': issues,
            'query': query,
        }

    return render(request, 'issue/issue_list.html', c)

def issue_edit(request, project, id=None):

    project = get_object_or_404(Project, name=project)

    if id:
        issue = get_object_or_404(Issue, project__name=project.name, id=id)
        init_data = {'title': issue.title,
                     'comment': issue.events.first().additionnal_section}
    else:
        issue = None
        init_data = None

    class IssueForm(forms.Form):

        title = forms.CharField(max_length=128)
        comment = forms.CharField(widget=MarkdownWidget)

    form = IssueForm(request.POST or init_data)

    if request.method == 'POST' and form.is_valid():

        title = form.cleaned_data['title']
        comment = form.cleaned_data['comment']
        print(comment)

        if issue:

            modified = False

            if issue.title != title:
                old_title = issue.title
                issue.title = title
                issue.save()
                author = User.objects.get(username=request.user.username)
                event = Event(issue=issue, author=author, code=Event.RENAME,
                        args={'old_title': old_title, 'new_title': title})
                event.save()
                modified = True

            first_comment = issue.events.first()
            if first_comment.additionnal_section != comment:
                first_comment.additionnal_section = comment
                first_comment.save()
                modified = True

            if modified:
                messages.success(request, 'Issue updated successfully.')
            else:
                messages.info(request, 'Issue not modified.')

        else:

            author = User.objects.get(username=request.user.username)
            issue = Issue(title=title, author=author,
                    project=project, id=Issue.next_id(project))
            issue.save()
            event = Event(issue=issue, author=author, code=Event.COMMENT,
                    additionnal_section=comment)
            event.save()
            messages.success(request, 'Issue created successfully.')

        return redirect('show-issue', project.name, issue.id)

    projects = Project.objects.all()

    c = {
            'request': request,
            'projects': projects,
            'project': project,
            'form': form,
        }

    return render(request, 'issue/issue_edit.html', c)

def issue(request, project, id):

    issue = get_object_or_404(Issue, project__name=project, id=id)

    projects = Project.objects.all()

    events = issue.events.all()

    c = {
            'request': request,
            'projects': projects,
            'project': issue.project,
            'issue': issue,
            'events': events,
        }

    return render(request, 'issue/issue.html', c)

def issue_comment(request, project, id, comment=None):

    issue = get_object_or_404(Issue, project__name=project, id=id)

    if comment:
        event = get_object_or_404(Event, code=Event.COMMENT, issue=issue, id=comment)
        init_data = {'comment': comment.additionnal_section}
    else:
        event = None
        init_data = None

    class CommentForm(forms.Form):

        comment = forms.CharField(widget=MarkdownWidget)

    form = CommentForm(request.POST or init_data)

    if request.method == 'POST' and form.is_valid():

        comment = form.cleaned_data['comment']

        if event:

            if event.additionnal_section != comment:
                event.additionnal_section = comment
                event.save()
                messages.success(request, 'Comment modified successfully.')
            else:
                messages.info(request, 'Comment not modified.')

        else:

            author = User.objects.get(username=request.user.username)
            event = Event(issue=issue, author=author, 
                    code=Event.COMMENT, additionnal_section=comment)
            event.save()
            messages.success(request, 'Comment added successfully.')

        return redirect('show-issue', issue.project.name, issue.id)

    projects = Project.objects.all()

    c = {
            'request': request,
            'projects': projects,
            'project': issue.project,
            'issue': issue,
            'form': form,
        }

    return render(request, 'issue/issue_comment.html', c)

def issue_close(request, project, id):

    issue = get_object_or_404(Issue, project__name=project, id=id, closed=False)

    issue.closed = True
    issue.save()

    author = User.objects.get(username=request.user.username)
    event = Event(issue=issue, author=author, code=Event.CLOSE)
    event.save()

    return redirect('list-issue', project)

def issue_reopen(request, project, id):

    issue = get_object_or_404(Issue, project__name=project, id=id, closed=True)

    issue.closed = False
    issue.save()

    author = User.objects.get(username=request.user.username)
    event = Event(issue=issue, author=author, code=Event.REOPEN)
    event.save()

    return redirect('show-issue', project, issue.id)

def issue_delete(request, project, id):

    issue = get_object_or_404(Issue, project__name=project, id=id)

    issue.delete()

    messages.success(request, 'Issue deleted successfully.')

    return redirect('list-issue', project)

def label_list(request, project):

    project = get_object_or_404(Project, name=project)

    labels = project.labels.all()

    projects = Project.objects.all()

    c = {
            'request': request,
            'projects': projects,
            'project': project,
            'labels': labels,
        }

    return render(request, 'issue/label_list.html', c)

def label_edit(request, project, label=None):

    project = get_object_or_404(Project, name=project)

    if label:
        label = get_object_or_404(Label, project=project, name=label)

    LabelForm = modelform_factory(Label, fields=['name', 'color'])
    form = LabelForm(request.POST or None, instance=label)

    if request.method == 'POST' and form.is_valid():

        if label:
            form.save()
            messages.success(request, 'Label modified successfully.')
        else:
            label = form.save(commit=False)
            label.project = project
            label.save()
            messages.success(request, 'Label added successfully.')

        return redirect('list-label', project.name)

    projects = Project.objects.all()

    c = {
            'request': request,
            'projects': projects,
            'project': project,
            'label': label,
            'form': form,
        }

    return render(request, 'issue/label_edit.html', c)

def milestone_list(request, project):

    project = get_object_or_404(Project, name=project)

    c = {
            'request': request,
            'project': project,
            'milestones': project.milestones.all(),
        }

    return render(request, 'issue/milestone_list.html', c)

def milestone_edit(request, project):

    project = get_object_or_404(Project, name=project)

    c = {
            'request': request,
            'project': project,
            'milestones': project.milestones.all(),
        }

    return render(request, 'issue/milestone_list.html', c)
