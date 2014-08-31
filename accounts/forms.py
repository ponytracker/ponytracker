from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput

from accounts.models import *


__all__ = ['UserForm', 'GroupForm', 'TeamForm']


UserForm = modelform_factory(User,
        fields=['username', 'first_name',
        'last_name', 'email', 'is_superuser'],
        widgets={'password': PasswordInput})
GroupForm = modelform_factory(Group,
        fields=['name'])
TeamForm = modelform_factory(Team,
        fields=['name'])
