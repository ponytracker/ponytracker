from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput

from permissions.models import *
from permissions.models import PermissionModel
from accounts.models import *


__all__ = [ 'GlobalPermissionForm', 'ProjectPermissionForm' ]


class PermissionForm(forms.ModelForm):

    class Meta:
        abstract = True

    # The grantee_id is a hidden field.
    # The user complete the grantee_name field, and the validation
    # method will set the correct value is the grantee_id.
    grantee_name = forms.CharField(max_length=32)

    def clean(self):

        data = super(PermissionForm, self).clean()

        if 'grantee_name' not in data or 'grantee_type' not in data:
            # a field required error will be printed so we dont care
            return data

        name = data['grantee_name']

        if int(data['grantee_type']) == PermissionModel.GRANTEE_USER:
            grantees = User.objects.filter(username=name)
            if not grantees.exists():
                raise ValidationError("User '%s' does not exists." % name)
        elif int(data['grantee_type']) == PermissionModel.GRANTEE_GROUP:
            grantees = Group.objects.filter(name=name)
            if not grantees.exists():
                raise ValidationError("Group '%s' does not exists." % name)
        elif int(data['grantee_type']) == PermissionModel.GRANTEE_TEAM:
            grantees = Team.objects.filter(name=name)
            if not grantees.exists():
                raise ValidationError("Team '%s' does not exists." % name)

        data['grantee_id'] = grantees.first().id

        return data


class GlobalPermissionForm(PermissionForm):

    class Meta:
        model = GlobalPermission
        fields =  [ 'grantee_type', 'grantee_id' ]
        widgets = {
                'grantee_id': HiddenInput,
        }


class ProjectPermissionForm(PermissionForm):

    class Meta:
        model = ProjectPermission
        # project is required for the unicity check
        fields =  [ 'project', 'grantee_type', 'grantee_id' ]
        widgets = {
            'project': HiddenInput,
            'grantee_id': HiddenInput,
        }
