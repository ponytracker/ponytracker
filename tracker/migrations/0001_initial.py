# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('code', models.IntegerField(default=0)),
                ('_args', models.CharField(default='{}', max_length=1024, blank=True)),
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
                ('primarykey', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.IntegerField(editable=False)),
                ('title', models.CharField(max_length=128)),
                ('opened_at', models.DateTimeField(auto_now_add=True)),
                ('closed', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='issue',
            field=models.ForeignKey(to='tracker.Issue'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('deleted', models.BooleanField(default=False)),
                ('color', colorful.fields.RGBColorField(default='#000000', verbose_name='Background color')),
                ('inverted', models.BooleanField(default=True, verbose_name='Inverse text color')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(null=True, to='tracker.Label', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.RegexValidator(regex='^[a-z0-9_.-]+$', message='Please enter only lowercase characters, number, dot, underscores or hyphens.')], max_length=32)),
                ('due_date', models.DateTimeField(null=True, blank=True)),
                ('closed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(to='tracker.Milestone', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('display_name', models.CharField(max_length=32, verbose_name='Project name', unique=True)),
                ('name', models.SlugField(max_length=32, verbose_name='URL name', unique=True)),
                ('description', models.TextField(default='', verbose_name='Description', blank=True)),
                ('access', models.IntegerField(default=1, choices=[(1, 'Public'), (2, 'Registration required'), (3, 'Private')])),
                ('subscribers', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(to='tracker.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='milestone',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AddField(
            model_name='label',
            name='project',
            field=models.ForeignKey(to='tracker.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(to='tracker.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together=set([('project', 'id')]),
        ),
    ]
