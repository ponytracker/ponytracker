# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0008_auto_20140808_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpermission',
            name='project',
            field=models.ForeignKey(editable=False, to='issue.Project'),
        ),
    ]
