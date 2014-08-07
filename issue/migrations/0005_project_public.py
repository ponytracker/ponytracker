# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0004_milestone_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='public',
            field=models.BooleanField(default=True, verbose_name='Do unregistered users have read access to this project?'),
            preserve_default=True,
        ),
    ]
