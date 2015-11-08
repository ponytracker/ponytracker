from django import forms

from tracker.models import *
from tracker.models import Settings


__all__ = [
    'SettingsForm', 'ProjectForm', 'LabelForm', 'IssueForm', 'MilestoneForm', 'CommentForm'
]


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        exclude = ('Site',)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['display_name', 'name', 'description', 'access']
        help_texts = {
            'name': 'Warning: if you change this value, '
                    'this will break existing URLs.'
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'due_date']
    description = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'color', 'inverted']


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'due_date']
