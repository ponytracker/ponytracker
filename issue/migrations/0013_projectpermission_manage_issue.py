# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0012_auto_20140812_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpermission',
            name='manage_issue',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
