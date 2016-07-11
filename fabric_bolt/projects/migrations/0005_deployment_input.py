# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20160312_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='input',
            field=models.TextField(null=True, blank=True),
        ),
    ]
