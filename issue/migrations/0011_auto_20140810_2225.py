# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0010_projectpermission_manage_permission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='globalpermission',
            old_name='manage_permission',
            new_name='manage_global_permission',
        ),
        migrations.RenameField(
            model_name='projectpermission',
            old_name='manage_permission',
            new_name='manage_project_permission',
        ),
    ]
