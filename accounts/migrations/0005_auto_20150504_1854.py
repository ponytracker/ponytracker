# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150412_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='teams+'),
        ),
    ]
