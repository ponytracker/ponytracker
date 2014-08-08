from django import forms
from django.forms.models import modelform_factory

from bootstrap3_datetime.widgets import DateTimePicker
from django_markdown.widgets import MarkdownWidget

from issue.models import *

AddProjectForm = modelform_factory(Project, fields=['display_name', 'name', 'description', 'public'])
EditProjectForm = modelform_factory(Project, fields=['display_name', 'description', 'public'])
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

class PermissionForm(forms.ModelForm):

    class Meta:
        model = PermissionModel
        exclude = []
        abstract = True

    def clean(self):

        data = super(PermissionForm, self).clean()

        if not 'grantee_name' in data or not 'grantee_type' in data:
            # a field required error will be printed so we dont care
            return data

        name = data['grantee_name']

        if int(data['grantee_type']) == PermissionModel.GRANTEE_USER:
            if not User.objects.filter(username=name).exists():
                raise ValidationError("User '%s' does not exists." %name)
        elif int(data['grantee_type']) == PermissionModel.GRANTEE_GROUP:
            if not Group.objects.filter(name=name).exists():
                raise ValidationError("Group '%s' does not exists." %name)
        elif int(data['grantee_type']) == PermissionModel.GRANTEE_TEAM:
            if not Team.objects.filter(name=name).exists():
                raise ValidationError("Team '%s' does not exists." %name)

        return data

class GlobalPermissionForm(PermissionForm):

    class Meta:
        model = GlobalPermission
        exclude = []

class ProjectPermissionForm(PermissionForm):

    class Meta:
        model = ProjectPermission
        exclude = []
