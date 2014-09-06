from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from tracker.models import *


__all__ = [
    'ProjectForm', 'LabelForm', 'IssueForm', 'MilestoneForm', 'CommentForm'
]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['display_name', 'name', 'description', 'access']
        help_texts = {
            'name': 'Warning: if you change this value, '
                    'this will break existing URLs.'
        }


class IssueForm(forms.Form):
    title = forms.CharField(max_length=128)
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
        widgets = {
            'due_date': DateTimePicker(format="%Y-%m-%d %H:%M"),
        }
