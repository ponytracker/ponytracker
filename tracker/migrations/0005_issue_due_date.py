# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_auto_20150412_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='due_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
