from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput

from accounts.models import *


__all__ = ['ProfileForm', 'GroupForm', 'TeamForm']


ProfileForm = modelform_factory(User,
        fields=['first_name', 'last_name', 'email', 'notifications'])
GroupForm = modelform_factory(Group,
        fields=['name'])
TeamForm = modelform_factory(Team,
        fields=['name'])
