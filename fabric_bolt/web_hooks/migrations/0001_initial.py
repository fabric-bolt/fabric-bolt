# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20140912_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('url', models.URLField()),
                ('project', models.ForeignKey(blank=True, to='projects.Project', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
