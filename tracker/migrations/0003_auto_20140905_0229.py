# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20140902_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='issue',
            field=models.ForeignKey(related_name='events', to='tracker.Issue'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='+'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='issues', null=True, to='tracker.Label'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(null=True, to='tracker.Milestone', blank=True, related_name='issues'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(related_name='issues', to='tracker.Project'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribed_issues', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='label',
            name='project',
            field=models.ForeignKey(related_name='labels', to='tracker.Project'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(related_name='milestones', to='tracker.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribed_projects', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
