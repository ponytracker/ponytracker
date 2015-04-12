# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20140905_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(related_name='issues', to='tracker.Label', blank=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribed_issues', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribed_projects', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
