# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('code', models.IntegerField(default=0)),
                ('_args', models.CharField(blank=True, default='{}', max_length=1024)),
                ('additionnal_section', models.TextField(blank=True, default='')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('global_id', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.IntegerField(editable=False)),
                ('title', models.CharField(max_length=128)),
                ('opened_at', models.DateTimeField(auto_now_add=True)),
                ('closed', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('deleted', models.BooleanField(default=False)),
                ('color', colorful.fields.RGBColorField(verbose_name='Background color', default='#000000')),
                ('inverted', models.BooleanField(default=True, verbose_name='Inverse text color')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(blank=True, to='issue.Label', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('name', models.CharField(primary_key=True, verbose_name='Short name (used in URL, definitive)', validators=[django.core.validators.RegexValidator(message='Please enter only lowercase characters, number, underscores or hyphens.', regex='^[a-z0-9_-]+$')], serialize=False, max_length=32)),
                ('display_name', models.CharField(verbose_name='Project name', unique=True, max_length=32)),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
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
