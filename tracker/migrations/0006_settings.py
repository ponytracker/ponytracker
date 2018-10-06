# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('tracker', '0005_issue_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('items_per_page', models.IntegerField(verbose_name='Items per page', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(500)], default=25)),
                ('site', models.OneToOneField(editable=False, related_name='settings', to='sites.Site', on_delete=models.CASCADE)),
            ],
        ),
    ]
