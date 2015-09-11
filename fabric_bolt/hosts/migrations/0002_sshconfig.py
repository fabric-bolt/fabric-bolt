# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fabric_bolt.core.mixins.storages


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
                ('private_key_file', models.FileField(storage=fabric_bolt.core.mixins.storages.FileStorageCHMOD600(), upload_to=b'private_keys')),
                ('remote_user', models.CharField(default=b'root', max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
