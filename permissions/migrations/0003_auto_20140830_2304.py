# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_auto_20140829_2335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='globalpermission',
            old_name='manage_user',
            new_name='manage_accounts',
        ),
        migrations.RemoveField(
            model_name='globalpermission',
            name='manage_group',
        ),
        migrations.RemoveField(
            model_name='globalpermission',
            name='manage_team',
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='project',
            field=models.ForeignKey(to='tracker.Project', on_delete=models.CASCADE),
        ),
    ]
