# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_milestone_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='project',
            field=models.ForeignKey(to='tracker.Project', related_name='+', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(to='tracker.Project', related_name='+', on_delete=models.CASCADE),
        ),
    ]
