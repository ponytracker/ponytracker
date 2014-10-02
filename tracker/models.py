from django.db import models
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django.utils.html import escape, format_html
from django.utils.encoding import python_2_unicode_compatible
from django import VERSION

from colorful.fields import RGBColorField

import json

from accounts.models import User

from tracker.templatetags.tracker_tags import *


__all__ = ['Project', 'Issue', 'Label', 'Milestone', 'Event']


@python_2_unicode_compatible
class Project(models.Model):

    class Meta:
        ordering = ['name']

    ACCESS_PUBLIC = 1
    ACCESS_REGISTERED = 2
    ACCESS_PRIVATE = 3
    ACCESS_TYPE = (
        (ACCESS_PUBLIC, 'Public'),
        (ACCESS_REGISTERED, 'Registration required'),
        (ACCESS_PRIVATE, 'Private'),
    )

    display_name = models.CharField(max_length=32, unique=True,
            verbose_name="Project name")

    name = models.SlugField(max_length=32, unique=True,
            verbose_name="URL name")

    description = models.TextField(blank=True, default="",
            verbose_name="Description")

    access = models.IntegerField(choices=ACCESS_TYPE, default=ACCESS_PUBLIC)

    subscribers = models.ManyToManyField(User, blank=True, null=True,
            related_name='subscribed_projects')

    def __str__(self):
        return self.display_name


@python_2_unicode_compatible
class Label(models.Model):

    project = models.ForeignKey(Project, related_name='labels')

    name = models.CharField(max_length=32)

    deleted = models.BooleanField(default=False)

    color = RGBColorField(default='#000000',
            verbose_name="Background color")

    inverted = models.BooleanField(default=True,
            verbose_name="Inverse text color")

    @property
    def quotted_name(self):
        if ' ' in self.name:
            name = '&quot;' + escape(self.name) + '&quot'
        else:
            name = escape(self.name)
        return mark_safe(name)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Milestone(models.Model):

    class Meta:
        ordering = ['due_date']
        unique_together = ['project', 'name']

    name_validator = RegexValidator(regex='^[a-z0-9_.-]+$',
            message="Please enter only lowercase characters, number, "
                    "dot, underscores or hyphens.")

    project = models.ForeignKey(Project, related_name='milestones')

    name = models.CharField(max_length=32, validators=[name_validator])

    due_date = models.DateTimeField(blank=True, null=True)

    closed = models.BooleanField(default=False)

    def closed_issues(self):

        return self.issues.filter(closed=True).count()

    def total_issues(self):

        return self.issues.count()

    def progress(self):

        closed = self.closed_issues()
        total = self.total_issues()

        if total:
            return int(100 * closed / total)
        else:
            return 0

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Issue(models.Model):

    # id is the id in the project, not the pk, so we need one
    primarykey = models.AutoField(primary_key=True)

    project = models.ForeignKey(Project, related_name='issues')
    id = models.IntegerField(editable=False)

    class Meta:
        unique_together = ['project', 'id']

    title = models.CharField(max_length=128)

    author = models.ForeignKey(User, related_name='+')

    opened_at = models.DateTimeField(auto_now_add=True)

    closed = models.BooleanField(default=False)

    labels = models.ManyToManyField(Label, blank=True, null=True,
            related_name='issues')

    milestone = models.ForeignKey(Milestone, blank=True, null=True,
            related_name='issues')

    assignee = models.ForeignKey(User, blank=True, null=True, related_name='+')

    subscribers = models.ManyToManyField(User, blank=True, null=True,
            related_name='subscribed_issues')

    @staticmethod
    def next_id(project):

        last_issue = project.issues.last()
        if last_issue:
            return last_issue.id + 1
        else:
            return 1

    @property
    def comments(self):

        return self.events.filter(code=Event.COMMENT)

    def getdesc(self):
        desc = self.events.filter(code=Event.DESCRIBE)
        if desc.exists():
            return desc.first().additionnal_section
        else:
            return None

    def setdesc(self, value):
        desc = self.events.filter(code=Event.DESCRIBE)
        if desc.exists():
            desc = desc.first()
            desc.additionnal_section = value
            desc.save()
        else:
            desc = Event(issue=self, author=self.author, code=Event.DESCRIBE,
                    additionnal_section=value)
            desc.save()

    def deldesc(self):
        desc = self.events.filter(code=Event.DESCRIBE)
        if desc.exists():
            desc.first().delete()
    description = property(getdesc, setdesc, deldesc)

    def add_label(self, author, label, commit=True):
        if self.labels.filter(pk=label.pk).exists():
            return
        self.labels.add(label)
        if commit:
            self.save()
        event = Event(issue=self, author=author,
                code=Event.ADD_LABEL, args={'label': label.id})
        event.save()

    def remove_label(self, author, label, commit=True):
        self.labels.remove(label)
        if commit:
            self.save()
        event = Event(issue=self, author=author,
                code=Event.DEL_LABEL, args={'label': label.id})
        event.save()

    def add_milestone(self, author, milestone, commit=True):
        if self.milestone == milestone:
            return
        if self.milestone:
            event = Event(issue=self, author=author,
                    code=Event.CHANGE_MILESTONE,
                    args={'old_milestone': self.milestone.name,
                          'new_milestone': milestone.name})
            event.save()
        else:
            event = Event(issue=self, author=author,
                    code=Event.SET_MILESTONE,
                    args={'milestone': milestone.name})
            event.save()
        self.milestone = milestone
        if commit:
            self.save()

    def remove_milestone(self, author, milestone, commit=True):
        self.milestone = None
        if commit:
            self.save()
        event = Event(issue=self, author=author,
                code=Event.UNSET_MILESTONE,
                args={'milestone': milestone.name})
        event.save()

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Event(models.Model):

    UNKNOW = 0
    CLOSE = 1
    REOPEN = 2
    RENAME = 3
    ADD_LABEL = 4
    DEL_LABEL = 5
    SET_MILESTONE = 6
    CHANGE_MILESTONE = 7
    UNSET_MILESTONE = 8
    REFERENCE = 9
    COMMENT = 10
    DESCRIBE = 11
    ASSIGN = 12
    UNASSIGN = 13

    issue = models.ForeignKey(Issue, related_name="%(class)ss")

    date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User)

    code = models.IntegerField(default=UNKNOW)

    _args = models.CharField(max_length=1024, blank=True, default="{}")

    def getargs(self):
        return json.loads(self._args)

    def setargs(self, args):
        self._args = json.dumps(args)

    def delargs(self):
        self._args = "{}"
    args = property(getargs, setargs, delargs)

    additionnal_section = models.TextField(blank=True, default="")

    def editable(self):

        return self.code == Event.COMMENT or self.code == Event.DESCRIBE

    def glyphicon(self):

        if self.code == Event.COMMENT:
            return "comment"
        elif self.code == Event.DESCRIBE:
            return "edit"
        elif self.code == Event.CLOSE:
            return "ban-circle"
        elif self.code == Event.REOPEN:
            return "refresh"
        elif self.code == Event.RENAME:
            return "transfer"
        elif self.code == Event.ADD_LABEL \
                or self.code == Event.DEL_LABEL:
            return "tag"
        elif self.code == Event.SET_MILESTONE \
                or self.code == Event.CHANGE_MILESTONE \
                or self.code == Event.UNSET_MILESTONE:
            return "road"
        elif self.code == Event.REFERENCE:
            return "transfer"
        elif self.code == Event.ASSIGN \
                or self.code == Event.UNASSIGN:
            return "user"
        else:
            return "cog"

    def __str__(self):

        args = self.args

        if self.code == Event.COMMENT or self.code == Event.DESCRIBE:
            description = "commented"
        elif self.code == Event.CLOSE:
            description = "closed this issue"
        elif self.code == Event.REOPEN:
            description = "reopened this issue"
        elif self.code == Event.RENAME:
            description = "changed the title from <mark>{old_title}</mark> " \
                          "to <mark>{new_title}</mark>"
        elif self.code == Event.ADD_LABEL or self.code == Event.DEL_LABEL:
            label = Label.objects.get(id=args['label'])
            if self.code == Event.ADD_LABEL:
                action = 'added'
            else:
                action = 'removed'
            description = '%s the <a href="%s" class="label" ' \
                          'style="%s">%s</a> label' \
                          % (action, same_label(label),
                             label_style(label), label)
        elif self.code == Event.SET_MILESTONE \
                or self.code == Event.UNSET_MILESTONE:
            milestone = Milestone(name=args['milestone'],
                    project=self.issue.project)
            if self.code == Event.SET_MILESTONE:
                action = 'added'
            else:
                action = 'removed'
            description = '%s this to the <span class="glyphicon ' \
                          'glyphicon-road"></span> <a href="%s">' \
                          '<b>{milestone}</b></a> milestone' \
                          % (action, same_milestone(milestone))
        elif self.code == Event.CHANGE_MILESTONE:
            old_ms = Milestone(name=args['old_milestone'],
                    project=self.issue.project)
            new_ms = Milestone(name=args['new_milestone'],
                    project=self.issue.project)
            description = 'moved this from the <span class="glyphicon ' \
                          'glyphicon-road"></span> <a href="%s">' \
                          '<b>{old_milestone}</b></a> milestone ' \
                          'to the <span class="glyphicon ' \
                          'glyphicon-road"></span> <a href="%s">' \
                          '<b>{new_milestone}</b></a> milestone' \
                          % (same_milestone(old_ms), same_milestone(new_ms))
        elif self.code == Event.REFERENCE:
            description = "referenced this issue"
        else:
            return None

        return format_html(description, **args)


if VERSION < (1, 7):
    import tracker.signals
