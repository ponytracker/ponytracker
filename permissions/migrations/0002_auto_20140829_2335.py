# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectpermission',
            unique_together=set([('project', 'grantee_type', 'grantee_id')]),
        ),
    ]
