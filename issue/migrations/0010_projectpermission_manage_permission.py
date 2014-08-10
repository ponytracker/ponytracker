# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0009_auto_20140808_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpermission',
            name='manage_permission',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
