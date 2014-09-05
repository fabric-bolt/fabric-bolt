# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_default_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Deployer')
    Group.objects.get_or_create(name='Historian')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_groups),
    ]
