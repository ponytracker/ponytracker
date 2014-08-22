# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields
from django.conf import settings
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=75)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('code', models.IntegerField(default=0)),
                ('_args', models.CharField(max_length=1024, default='{}', blank=True)),
                ('additionnal_section', models.TextField(blank=True, default='')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('grantee_type', models.IntegerField(choices=[(0, 'User'), (1, 'Group'), (2, 'Team')], verbose_name='Type', default=0)),
                ('grantee_name', models.CharField(verbose_name='Name', max_length=50)),
                ('create_project', models.BooleanField(default=True)),
                ('modify_project', models.BooleanField(default=False)),
                ('delete_project', models.BooleanField(default=False)),
                ('add_team', models.BooleanField(default=True)),
                ('manage_team', models.BooleanField(default=False)),
                ('manage_global_permission', models.BooleanField(default=False)),
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
            ],
            options={
                'abstract': False,
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
                ('assignee', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('deleted', models.BooleanField(default=False)),
                ('color', colorful.fields.RGBColorField(verbose_name='Background color', default='#000000')),
                ('inverted', models.BooleanField(verbose_name='Inverse text color', default=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(regex='^[a-z0-9_.-]+$', message='Please enter only lowercase characters, number, dot, underscores or hyphens.')])),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('closed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(blank=True, to='issue.Milestone', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(primary_key=True, verbose_name='Short name (used in URL, definitive)', validators=[django.core.validators.RegexValidator(regex='^[a-z0-9_-]+$', message='Please enter only lowercase characters, number, underscores or hyphens.')], serialize=False, max_length=32)),
                ('display_name', models.CharField(unique=True, verbose_name='Project name', max_length=32)),
                ('description', models.TextField(verbose_name='Description', default='', blank=True)),
                ('public', models.BooleanField(verbose_name='Do unregistered users have read access to this project?', default=True)),
                ('subscribers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
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
        migrations.CreateModel(
            name='ProjectPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('grantee_type', models.IntegerField(choices=[(0, 'User'), (1, 'Group'), (2, 'Team')], verbose_name='Type', default=0)),
                ('grantee_name', models.CharField(verbose_name='Name', max_length=50)),
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
                ('project', models.ForeignKey(editable=False, to='issue.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', null=True)),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
