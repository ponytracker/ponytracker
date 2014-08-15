# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0013_projectpermission_manage_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalpermission',
            name='create_comment',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='create_issue',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='delete_comment',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='delete_issue',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='delete_tags',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='manage_issue',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='manage_project_permission',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='manage_tags',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='modify_comment',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='modify_issue',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
