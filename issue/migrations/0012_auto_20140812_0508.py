# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0011_auto_20140810_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpermission',
            name='delete_tags',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectpermission',
            name='manage_tags',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='projectpermission',
            name='create_label',
        ),
        migrations.RemoveField(
            model_name='projectpermission',
            name='create_milestone',
        ),
        migrations.RemoveField(
            model_name='projectpermission',
            name='delete_label',
        ),
        migrations.RemoveField(
            model_name='projectpermission',
            name='delete_milestone',
        ),
        migrations.RemoveField(
            model_name='projectpermission',
            name='modify_label',
        ),
        migrations.RemoveField(
            model_name='projectpermission',
            name='modify_milestone',
        ),
    ]
