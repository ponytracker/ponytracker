# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0003_auto_20140803_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
