# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(to='issue.Milestone', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='progression',
        ),
    ]
