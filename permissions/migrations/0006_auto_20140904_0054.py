# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import permissions.models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0005_auto_20140902_0521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalpermission',
            name='access_project',
            field=permissions.models.ProjectPermissionField(verbose_name='Access all project', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='create_comment',
            field=permissions.models.ProjectPermissionField(verbose_name='Create comment', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='create_issue',
            field=permissions.models.ProjectPermissionField(verbose_name='Create issue', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='delete_comment',
            field=permissions.models.ProjectPermissionField(verbose_name='Delete comment', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='delete_issue',
            field=permissions.models.ProjectPermissionField(verbose_name='Delete issue', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='delete_project',
            field=permissions.models.GlobalPermissionField(verbose_name='Delete project', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='delete_tags',
            field=permissions.models.ProjectPermissionField(verbose_name='Delete labels and milestones', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='grantee_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='manage_accounts',
            field=permissions.models.GlobalPermissionField(verbose_name='Manage users, groups and teams', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='manage_global_permission',
            field=permissions.models.GlobalPermissionField(verbose_name='Manage global permissions', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='manage_issue',
            field=permissions.models.ProjectPermissionField(verbose_name='Manage issue', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='manage_project_permission',
            field=permissions.models.ProjectPermissionField(verbose_name='Manage project permissions', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='manage_settings',
            field=permissions.models.GlobalPermissionField(verbose_name='Manage settings', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='manage_tags',
            field=permissions.models.ProjectPermissionField(verbose_name='Assign and remove labels and milestones', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='modify_comment',
            field=permissions.models.ProjectPermissionField(verbose_name='Modify comment', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='modify_issue',
            field=permissions.models.ProjectPermissionField(verbose_name='Modify issue', default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='modify_project',
            field=permissions.models.GlobalPermissionField(verbose_name='Modify project', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='create_comment',
            field=permissions.models.PermissionField(verbose_name='Create comment', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='create_issue',
            field=permissions.models.PermissionField(verbose_name='Create issue', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='delete_comment',
            field=permissions.models.PermissionField(verbose_name='Delete comment', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='delete_issue',
            field=permissions.models.PermissionField(verbose_name='Delete issue', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='delete_tags',
            field=permissions.models.PermissionField(verbose_name='Delete labels and milestones', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='grantee_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='manage_issue',
            field=permissions.models.PermissionField(verbose_name='Manage issue', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='manage_project_permission',
            field=permissions.models.PermissionField(verbose_name='Manage project permissions', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='manage_tags',
            field=permissions.models.PermissionField(verbose_name='Assign and remove labels and milestones', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='modify_comment',
            field=permissions.models.PermissionField(verbose_name='Modify comment', default=False),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='modify_issue',
            field=permissions.models.PermissionField(verbose_name='Modify issue', default=False),
        ),
    ]
