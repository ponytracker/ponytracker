# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import re
import colorful.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('code', models.IntegerField(default=0)),
                ('_args', models.CharField(default='{}', blank=True, max_length=1024)),
                ('additionnal_section', models.TextField(default='', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('global_id', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.IntegerField(editable=False)),
                ('title', models.CharField(max_length=128)),
                ('opened_at', models.DateTimeField(auto_now=True)),
                ('closed', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='issue',
            field=models.ForeignKey(to='issue.Issue'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('color', colorful.fields.RGBColorField(default='#FFFFFF')),
                ('inverted', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, to='issue.Label'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('progression', models.SmallIntegerField(default=0)),
                ('due_date', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(serialize=False, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+$', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], primary_key=True, max_length=32, verbose_name='Short name (used in URL)')),
                ('display_name', models.CharField(max_length=32, verbose_name='Project name')),
                ('description', models.TextField(default='', blank=True, verbose_name='Description')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(to='issue.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='milestone',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AddField(
            model_name='label',
            name='project',
            field=models.ForeignKey(to='issue.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(to='issue.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together=set([('project', 'id')]),
        ),
    ]
