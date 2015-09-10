# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSHConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('public_key', models.TextField()),
                ('private_key_file', models.CharField(max_length=1500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
