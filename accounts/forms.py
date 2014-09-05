from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput

from accounts.models import *


__all__ = ['UserForm', 'UserFormWithoutUsername', 'ProfileForm', 'GroupForm', 'TeamForm']


user_fields=['first_name', 'last_name', 'email', 'notifications']

UserForm = modelform_factory(User,
        fields=['username']+user_fields+['is_superuser'])
UserFormWithoutUsername = modelform_factory(User,
        fields=user_fields+['is_superuser'])
ProfileForm = modelform_factory(User,
        fields=user_fields)
GroupForm = modelform_factory(Group,
        fields=['name'])
TeamForm = modelform_factory(Team,
        fields=['name'])
