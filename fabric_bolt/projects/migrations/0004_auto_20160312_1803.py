# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20150911_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='data_type',
            field=models.CharField(default=b'string', choices=[(b'boolean', b'Boolean'), (b'number', b'Number'), (b'string', b'String'), (b'ssh_key', b'SSH Key')], max_length=10, blank=True, null=True, verbose_name=b'Type'),
        ),
    ]
