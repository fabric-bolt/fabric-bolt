# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=500, null=True, blank=True)),
                ('value_number', models.FloatField(default=0, null=True, verbose_name=b'Value', blank=True)),
                ('value_boolean', models.BooleanField(default=False, verbose_name=b'Value')),
                ('data_type', models.CharField(default=b'string', max_length=10, null=True, blank=True, choices=[(b'boolean', b'Boolean'), (b'number', b'Number'), (b'string', b'String')])),
                ('task_name', models.CharField(help_text=b'The name of the task this argument should be used on.', max_length=255, null=True, blank=True)),
                ('prompt_me_for_input', models.BooleanField(default=False, help_text=b'When deploying you will be prompted for this value.')),
                ('sensitive_value', models.BooleanField(default=False, help_text=b'Password or other value that should not be stored in the logs.')),
                ('task_argument', models.BooleanField(default=False, help_text=b'"Configuration" should be passed as a task argument rather than set on env.')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('comments', models.TextField()),
                ('status', models.CharField(default=b'pending', max_length=10, choices=[(b'pending', b'Pending'), (b'failed', b'Failed'), (b'success', b'Success')])),
                ('output', models.TextField(null=True, blank=True)),
                ('configuration', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [b'-date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('use_repo_fabfile', models.BooleanField(default=False, help_text=b'If no, use the default fabfile.', verbose_name=b"Use repo's fabfile?")),
                ('repo_url', models.CharField(help_text=b'Currently only git repos are supported.', max_length=200, null=True, blank=True)),
                ('fabfile_requirements', models.TextField(help_text=b'Pip requirements to install for fabfile. Enter one requirement per line.', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='configuration',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.ForeignKey(blank=True, to='projects.ProjectType', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('hosts', models.ManyToManyField(to='hosts.Host')),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deployment',
            name='stage',
            field=models.ForeignKey(to='projects.Stage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='configuration',
            name='stage',
            field=models.ForeignKey(blank=True, to='projects.Stage', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('times_used', models.PositiveIntegerField(default=1)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deployment',
            name='task',
            field=models.ForeignKey(to='projects.Task'),
            preserve_default=True,
        ),
    ]
