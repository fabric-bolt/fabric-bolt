# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fabric_bolt.hosts.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'DNS name or IP address', max_length=255, validators=[fabric_bolt.hosts.models.full_domain_validator])),
                ('alias', models.CharField(blank=True, max_length=255, null=True, help_text=b'Human readable value (optional)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
