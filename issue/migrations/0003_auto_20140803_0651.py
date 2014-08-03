# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_auto_20140803_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='name',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='^[a-z0-9_.-]+$', message='Please enter only lowercase characters, number, dot, underscores or hyphens.')], max_length=32),
        ),
    ]
