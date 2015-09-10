# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0002_sshconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sshconfig',
            name='private_key_file',
            field=models.FileField(upload_to=b'private_keys'),
        ),
    ]
