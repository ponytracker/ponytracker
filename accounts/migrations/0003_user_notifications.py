# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20140905_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notifications',
            field=models.IntegerField(choices=[(0, 'Never'), (1, 'Ignore my actions'), (2, 'Always')], default=1),
            preserve_default=True,
        ),
    ]
