# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
