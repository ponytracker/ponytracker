from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.urlresolvers import reverse

import json

from colorful.fields import RGBColorField


class Project(models.Model):

    url_name_validator = RegexValidator(regex='^[a-z0-9_-]+$',
            message="Please enter only lowercase characters, number, "
                    "underscores or hyphens.")

    name = models.CharField(primary_key=True, blank=False, max_length=32,
            verbose_name="Short name (used in URL, definitive)",
            validators=[url_name_validator])

    display_name = models.CharField(max_length=32, unique=True,
            verbose_name="Project name")

    description = models.TextField(blank=True, default="",
            verbose_name="Description")

    def create_default_labels(self):

        Label(project=self, name='bug', color='#FF0000').save()
        Label(project=self, name='feature', color='#00A000').save()
        Label(project=self, name='documentation', color='#1D3DBE').save()

    def __str__(self):

        return self.display_name

class Label(models.Model):

    project = models.ForeignKey(Project, related_name='labels')

    name = models.CharField(max_length=32)

    deleted = models.BooleanField(default=False)

    color = RGBColorField(default='#000000', verbose_name="Background color")

    inverted = models.BooleanField(default=True, verbose_name="Inverse text color")

    def style(self):

        style = "background-color: {bg}; color: {fg};"
        
        if self.inverted:
            fg = '#fff'
        else:
            fg = '#000'

        return style.format(bg=self.color, fg=fg)

    def __str__(self):
        return self.name

class Milestone(models.Model):

    name_validator = RegexValidator(regex='^[a-z0-9_.-]+$',
            message="Please enter only lowercase characters, number, "
                    "dot, underscores or hyphens.")

    project = models.ForeignKey(Project, related_name='milestones')

    name = models.CharField(max_length=32, validators=[name_validator])

    class Meta:
        unique_together = [ 'project', 'name' ]

    due_date = models.DateTimeField(blank=True,null=True)

    def closed_issues(self):

        return self.issues.filter(closed=True).count()

    def total_issues(self):

        return self.issues.count()

    def progress(self):

        closed = self.closed_issues()
        total = self.total_issues()

        if total:
            return int(100 * closed / total);
        else:
            return 0

    def __str__(self):
        return self.name

class Issue(models.Model):

    global_id = models.AutoField(primary_key=True)
    
    project = models.ForeignKey(Project, related_name='issues')
    id = models.IntegerField(editable=False)

    class Meta:
        unique_together = [ 'project', 'id' ]

    title = models.CharField(max_length=128)

    author = models.ForeignKey(User, related_name='+')

    opened_at = models.DateTimeField(auto_now_add=True)

    closed = models.BooleanField(default=False)

    labels = models.ManyToManyField(Label, blank=True, null=True, related_name='issues')

    milestone = models.ForeignKey(Milestone, blank=True, null=True, related_name='issues')

    assignee = models.ForeignKey(User, blank=True, null=True, related_name='+')

    @staticmethod
    def next_id(project):

        last_issue = project.issues.last()
        if last_issue:
            return last_issue.id + 1
        else:
            return 1

    def comments(self):

        comments = self.events.filter(issue=self,code=Event.COMMENT)

        return comments

    def getdesc(self):
        desc = self.events.filter(issue=self,code=Event.DESCRIBE)
        if desc.count():
            return desc.first().additionnal_section
        else:
            return None
    def setdesc(self, value):
        desc = self.events.filter(issue=self,code=Event.DESCRIBE)
        if desc.count():
            desc = desc.first()
            desc.additionnal_section = value
            desc.save()
        else:
            desc = Event(issue=self, author=self.author, code=Event.DESCRIBE,
                    additionnal_section=value)
            desc.save()
    def deldesc(self):
        desc = self.events.filter(issue=self,code=Event.DESCRIBE)
        if desc.count():
            desc.first().delete()
    description = property(getdesc, setdesc, deldesc)

    def add_label(self, author, label, commit=True):
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
        if self.milestone:
            event = Event(issue=self, author=author, code=Event.CHANGE_MILESTONE,
                    args={'old_milestone': self.milestone.name,
                          'new_milestone': milestone.name})
            event.save()
        else:
            event = Event(issue=self, author=author, code=Event.SET_MILESTONE,
                    args={'milestone': milestone.name})
            event.save()
        self.milestone = milestone
        if commit:
            self.save()

    def remove_milestone(self, author, milestone, commit=True):
        self.milestone = None
        if commit:
            self.save()
        event = Event(issue=self, author=author, code=Event.UNSET_MILESTONE,
                args={'milestone': milestone.name})
        event.save()

    def __str__(self):
        return self.title

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
            description = "changed the title from <mark>{old_title}</mark> to <mark>{new_title}</mark>"
        elif self.code == Event.ADD_LABEL or self.code == Event.DEL_LABEL:
            label = Label.objects.get(id=args['label'])
            description = '{action} the <a href="{url}?q=is:open%20label:{label}"><span class="label" style="{style}">{label}</span></a> label'
            args['label'] = label.name
            args['url'] = reverse('list-issue', kwargs={'project': self.issue.project.name})
            args['style'] = label.style()
            if self.code == Event.ADD_LABEL:
                args['action'] = 'added'
            else:
                args['action'] = 'removed'
        elif self.code == Event.SET_MILESTONE:
            description = "added this to the {milestone} milestone"
        elif self.code == Event.CHANGE_MILESTONE:
            description = "moved this from the {old_milestone} milestone to the {new_milestone} milestone"
        elif self.code == Event.UNSET_MILESTONE:
            description = "deleted this from the {milestone} milestone"
        elif self.code == Event.REFERENCE:
            description = "referenced this issue"
        else:
            return None

        # Escape args
        safe_args = {k: escape(v) for k, v in args.items()}

        return mark_safe(description.format(**safe_args))
