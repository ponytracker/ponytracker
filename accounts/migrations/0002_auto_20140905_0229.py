# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='teams', null=True, to='accounts.Group'),
        ),
        migrations.AlterField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='+', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', blank=True, related_query_name='user', verbose_name='groups', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', related_name='user_set', blank=True, related_query_name='user', verbose_name='user permissions', to='auth.Permission'),
        ),
    ]
