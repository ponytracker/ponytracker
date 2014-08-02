from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug

import json

from colorful.fields import RGBColorField


class Project(models.Model):

    name = models.CharField(primary_key=True, blank=False, max_length=32,
            verbose_name="Short name (used in URL)",
            validators=[validate_slug])

    display_name = models.CharField(max_length=32,
            verbose_name="Project name")

    description = models.TextField(blank=True, default="",
            verbose_name="Description")

    def __str__(self):
        return self.display_name

class Label(models.Model):

    project = models.ForeignKey(Project, related_name='labels')

    name = models.CharField(max_length=32)

    class Meta:
        unique_together = [ 'project', 'name' ]

    color = RGBColorField(default='#FFFFFF')

    inverted = models.BooleanField(default=True)

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

    project = models.ForeignKey(Project, related_name='milestones')

    name = models.CharField(max_length=32)

    class Meta:
        unique_together = [ 'project', 'name' ]

    progression = models.SmallIntegerField(default=0)

    due_date = models.DateTimeField(null=True)

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

    opened_at = models.DateTimeField(auto_now=True)

    closed = models.BooleanField(default=False)

    labels = models.ManyToManyField(Label, blank=True, null=True)

    assignee = models.ForeignKey(User, blank=True, null=True, related_name='+')

    @staticmethod
    def next_id(project):

        last_issue = project.issues.last()
        if last_issue:
            return last_issue.id + 1
        else:
            return 1

    def comments(self):

        comments = self.events.filter(code=Event.COMMENT)

        return comments[1:]

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
    DEL_MILESTONE = 8
    REFERENCE = 9
    COMMENT = 10

    issue = models.ForeignKey(Issue, related_name="%(class)ss")

    date = models.DateTimeField(auto_now=True)

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

    def boxed(self):
        return self.code == Event.COMMENT

    def __str__(self):

        args = self.args

        if self.code == Event.COMMENT:
            description = "{author} commented"
        elif self.code == Event.CLOSE:
            description = "{author} closed this issue"
        elif self.code == Event.REOPEN:
            description = "{author} reopened this issue"
        elif self.code == Event.RENAME:
            description = "{author} changed the title from {old_title} to {new_title}"
        elif self.code == Event.ADD_LABEL:
            description = "{author} added the {label} label"
        elif self.code == Event.DEL_LABEL:
            description = "{author} deleted the {label} label"
        elif self.code == Event.SET_MILESTONE:
            description = "{author} added this to the {milestone} milestone"
        elif self.code == Event.CHANGE_MILESTONE:
            description = "{author} moved this from the {old_milestone} milestone to the {new_mileston} milestone"
        elif self.code == Event.DEL_MILESTONE:
            description = "{author} deleted this from the {milestone} milestone"
        elif self.code == Event.REFERENCE:
            description = "{author} referenced this issue"
        else:
            return None

        return description.format(author=self.author, **args)
