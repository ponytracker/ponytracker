from django import forms
from django.forms.models import modelform_factory

from bootstrap3_datetime.widgets import DateTimePicker
from django_markdown.widgets import MarkdownWidget

from issue.models import *


AddProjectForm = modelform_factory(Project, fields=['display_name', 'name', 'description'])
EditProjectForm = modelform_factory(Project, fields=['display_name', 'description'])
LabelForm = modelform_factory(Label, fields=['name', 'color', 'inverted'])

class MilestoneForm(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = ['name', 'due_date']
        widgets = { 
                'due_date': DateTimePicker(format="YYYY-MM-DD HH:mm"),
        }

class IssueForm(forms.Form):
    title = forms.CharField(max_length=128)
    description = forms.CharField(widget=MarkdownWidget, required=False)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=MarkdownWidget)
