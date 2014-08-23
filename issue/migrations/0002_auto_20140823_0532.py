# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='access',
            field=models.IntegerField(choices=[(1, 'Public'), (2, 'Connected users'), (3, 'Private')], default=1),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='project',
            name='public',
        ),
    ]
