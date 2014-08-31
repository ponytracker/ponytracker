from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django import VERSION

from tracker.models import Project
from accounts.models import *


__all__ = ['GlobalPermission', 'ProjectPermission']


@python_2_unicode_compatible
class PermissionModel(models.Model):

    GRANTEE_USER = 0
    GRANTEE_GROUP = 1
    GRANTEE_TEAM = 2
    GRANTEE_TYPE = (
        (GRANTEE_USER, 'User'),
        (GRANTEE_GROUP, 'Group'),
        (GRANTEE_TEAM, 'Team'),
    )

    grantee_type = models.IntegerField(choices=GRANTEE_TYPE,
            default=GRANTEE_USER, verbose_name="Grantee type")
    grantee_id = models.IntegerField(blank=True)

    def get_grantee(self):
        if self.grantee_type == self.GRANTEE_USER:
            Model = User
        elif self.grantee_type == self.GRANTEE_GROUP:
            Model = Group
        else:
            Model = Team
        return Model.objects.get(id=self.grantee_id)

    def set_grantee(self, grantee):
        if isinstance(grantee, User):
            self.grantee_type = self.GRANTEE_USER
        elif isinstance(grantee, Group):
            self.grantee_type = self.GRANTEE_GROUP
        elif isinstance(grantee, Team):
            self.grantee_type = self.GRANTEE_TEAM
        else:
            raise ValueError('Grantee object must be '
                    'an User, a Group or a Team instance.')
        self.grantee_id = grantee.id

    grantee = property(get_grantee, set_grantee)

    class Meta:
        abstract = True

    def granted_to(self, user):
        if not user.is_authenticated():
            return False
        if self.grantee_type == self.GRANTEE_USER:
            return user.id == self.grantee_id
        elif self.grantee_type == self.GRANTEE_GROUP:
            return user.groups.filter(id=self.grantee_id).exists()
        elif self.grantee_type == self.GRANTEE_TEAM:
            return Team.objects.filter(id=self.grantee_id) \
                .filter(Q(groups__in=user.groups.all()) | Q(users=user)) \
                .exists()
        else:
            return False

    @property
    def type(self):
        return self.get_grantee_type_display()

    @property
    def name(self):
        return self.grantee.__str__()

    def __str__(self):
        return self.grantee.__str__() + "'s permissions"


@python_2_unicode_compatible
class GlobalPermission(PermissionModel):

    class Meta:
        unique_together = ('grantee_type', 'grantee_id')

    # Global permissions

    create_project = models.BooleanField(default=True)
    modify_project = models.BooleanField(default=False)
    delete_project = models.BooleanField(default=False)

    manage_settings = models.BooleanField(default=False)
    manage_accounts = models.BooleanField(default=False)
    manage_global_permission = models.BooleanField(default=False)

    # Project permissions, given on ALL projects

    create_issue = models.BooleanField(default=True)
    modify_issue = models.BooleanField(default=False)
    manage_issue = models.BooleanField(default=False)
    delete_issue = models.BooleanField(default=False)

    create_comment = models.BooleanField(default=True)
    modify_comment = models.BooleanField(default=False)
    delete_comment = models.BooleanField(default=False)

    manage_tags = models.BooleanField(default=False)
    delete_tags = models.BooleanField(default=False)

    manage_project_permission = models.BooleanField(default=False)

    def __str__(self):
        return self.grantee.__str__() + "'s global permissions"


@python_2_unicode_compatible
class ProjectPermission(PermissionModel):

    class Meta:
        unique_together = ('project', 'grantee_type', 'grantee_id')

    project = models.ForeignKey(Project, related_name='permissions')

    manage_project_permission = models.BooleanField(default=False)

    create_issue = models.BooleanField(default=True)
    modify_issue = models.BooleanField(default=False)
    manage_issue = models.BooleanField(default=False)
    delete_issue = models.BooleanField(default=False)

    create_comment = models.BooleanField(default=True)
    modify_comment = models.BooleanField(default=False)
    delete_comment = models.BooleanField(default=False)

    manage_tags = models.BooleanField(default=False)
    delete_tags = models.BooleanField(default=False)

    def __str__(self):
        return self.grantee.__str__() + "'s permissions on " \
            + self.project.name + " project"


if VERSION < (1, 7):
    import tracker.signals
