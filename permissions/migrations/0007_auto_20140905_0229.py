# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0006_auto_20140904_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpermission',
            name='project',
            field=models.ForeignKey(related_name='permissions', to='tracker.Project'),
        ),
    ]
