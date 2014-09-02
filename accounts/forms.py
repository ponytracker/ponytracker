from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput

from accounts.models import *


__all__ = ['AddUserForm', 'EditUserForm', 'GroupForm', 'TeamForm']


user_fields=['first_name', 'last_name', 'email', 'is_superuser']

AddUserForm = modelform_factory(User,
        fields=['username']+user_fields)
EditUserForm = modelform_factory(User,
        fields=user_fields)
GroupForm = modelform_factory(Group,
        fields=['name'])
TeamForm = modelform_factory(Team,
        fields=['name'])
