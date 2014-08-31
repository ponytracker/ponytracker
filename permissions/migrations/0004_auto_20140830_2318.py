# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_auto_20140830_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalpermission',
            name='access_project',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='create_comment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='create_issue',
            field=models.BooleanField(default=False),
        ),
    ]
