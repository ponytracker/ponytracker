# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('grantee_type', models.IntegerField(default=0, verbose_name='Grantee type', choices=[(0, 'User'), (1, 'Group'), (2, 'Team')])),
                ('grantee_id', models.IntegerField(blank=True)),
                ('create_project', models.BooleanField(default=True)),
                ('modify_project', models.BooleanField(default=False)),
                ('delete_project', models.BooleanField(default=False)),
                ('manage_settings', models.BooleanField(default=False)),
                ('manage_user', models.BooleanField(default=False)),
                ('manage_group', models.BooleanField(default=False)),
                ('manage_team', models.BooleanField(default=False)),
                ('manage_global_permission', models.BooleanField(default=False)),
                ('create_issue', models.BooleanField(default=True)),
                ('modify_issue', models.BooleanField(default=False)),
                ('manage_issue', models.BooleanField(default=False)),
                ('delete_issue', models.BooleanField(default=False)),
                ('create_comment', models.BooleanField(default=True)),
                ('modify_comment', models.BooleanField(default=False)),
                ('delete_comment', models.BooleanField(default=False)),
                ('manage_tags', models.BooleanField(default=False)),
                ('delete_tags', models.BooleanField(default=False)),
                ('manage_project_permission', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='globalpermission',
            unique_together=set([('grantee_type', 'grantee_id')]),
        ),
        migrations.CreateModel(
            name='ProjectPermission',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('grantee_type', models.IntegerField(default=0, verbose_name='Grantee type', choices=[(0, 'User'), (1, 'Group'), (2, 'Team')])),
                ('grantee_id', models.IntegerField(blank=True)),
                ('manage_project_permission', models.BooleanField(default=False)),
                ('create_issue', models.BooleanField(default=True)),
                ('modify_issue', models.BooleanField(default=False)),
                ('manage_issue', models.BooleanField(default=False)),
                ('delete_issue', models.BooleanField(default=False)),
                ('create_comment', models.BooleanField(default=True)),
                ('modify_comment', models.BooleanField(default=False)),
                ('delete_comment', models.BooleanField(default=False)),
                ('manage_tags', models.BooleanField(default=False)),
                ('delete_tags', models.BooleanField(default=False)),
                ('project', models.ForeignKey(editable=False, to='tracker.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='projectpermission',
            unique_together=set([('grantee_type', 'grantee_id')]),
        ),
    ]
