# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('sites', '0001_initial'),
        ('issue', '0005_project_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('grantee', models.CharField(max_length=50)),
                ('create_project', models.BooleanField(default=True)),
                ('modify_project', models.BooleanField(default=False)),
                ('delete_project', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('grantee', models.CharField(max_length=50)),
                ('create_issue', models.BooleanField(default=True)),
                ('modify_issue', models.BooleanField(default=False)),
                ('delete_issue', models.BooleanField(default=False)),
                ('create_comment', models.BooleanField(default=True)),
                ('modify_comment', models.BooleanField(default=False)),
                ('delete_comment', models.BooleanField(default=False)),
                ('create_label', models.BooleanField(default=True)),
                ('modify_label', models.BooleanField(default=False)),
                ('delete_label', models.BooleanField(default=False)),
                ('create_milestone', models.BooleanField(default=True)),
                ('modify_milestone', models.BooleanField(default=False)),
                ('delete_milestone', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('project', models.ForeignKey(to='issue.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True, null=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
        migrations.AlterField(
            model_name='event',
            name='author',
            field=models.ForeignKey(to='issue.User'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(to='issue.User', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(to='issue.User'),
        ),
    ]
