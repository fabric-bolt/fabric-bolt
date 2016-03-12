# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150813_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployuser',
            name='email',
            field=models.EmailField(unique=True, max_length=255, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='deployuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
