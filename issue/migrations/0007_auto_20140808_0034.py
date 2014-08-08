# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0006_auto_20140807_2032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='globalpermission',
            old_name='grantee',
            new_name='grantee_name',
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='grantee_type',
            field=models.IntegerField(default=0, choices=[(0, 'User'), (1, 'Group'), (2, 'Team')]),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='projectpermission',
            old_name='grantee',
            new_name='grantee_name',
        ),
        migrations.AddField(
            model_name='projectpermission',
            name='grantee_type',
            field=models.IntegerField(default=0, choices=[(0, 'User'), (1, 'Group'), (2, 'Team')]),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='globalpermission',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='projectpermission',
            name='content_type',
        ),
    ]
