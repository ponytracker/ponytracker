# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0014_auto_20140815_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='subscribers',
            field=models.ManyToManyField(to='issue.User', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='subscribers',
            field=models.ManyToManyField(to='issue.User', blank=True, null=True),
            preserve_default=True,
        ),
    ]
