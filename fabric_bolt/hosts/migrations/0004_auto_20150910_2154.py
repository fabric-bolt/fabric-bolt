# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fabric_bolt.core.mixins.storages


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0003_auto_20150910_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='sshconfig',
            name='remote_user',
            field=models.CharField(default=b'root', max_length=100),
        ),
        migrations.AlterField(
            model_name='sshconfig',
            name='private_key_file',
            field=models.FileField(storage=fabric_bolt.core.mixins.storages.FileStorageCHMOD600(), upload_to=b'private_keys'),
        ),
    ]
