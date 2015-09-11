# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0002_sshconfig'),
        ('projects', '0002_auto_20140912_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='value_ssh_key',
            field=models.ForeignKey(verbose_name=b'Value', blank=True, to='hosts.SSHConfig', null=True),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='data_type',
            field=models.CharField(default=b'string', max_length=10, null=True, blank=True, choices=[(b'boolean', b'Boolean'), (b'number', b'Number'), (b'string', b'String'), (b'ssk_key', b'SSH Key')]),
        ),
    ]
