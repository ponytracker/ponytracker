# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0007_auto_20140808_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalpermission',
            name='add_team',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='manage_permission',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalpermission',
            name='manage_team',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='grantee_name',
            field=models.CharField(verbose_name='Name', max_length=50),
        ),
        migrations.AlterField(
            model_name='globalpermission',
            name='grantee_type',
            field=models.IntegerField(default=0, verbose_name='Type', choices=[(0, 'User'), (1, 'Group'), (2, 'Team')]),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='grantee_name',
            field=models.CharField(verbose_name='Name', max_length=50),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='grantee_type',
            field=models.IntegerField(default=0, verbose_name='Type', choices=[(0, 'User'), (1, 'Group'), (2, 'Team')]),
        ),
    ]
