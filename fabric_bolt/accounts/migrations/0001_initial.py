# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeployUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address', db_index=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.  Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('template', models.CharField(default=b'yeti.min.css', max_length=255, blank=True, choices=[(b'amelia.min.css', b'Amelia'), (b'cerulean.min.css', b'Cerulean'), (b'cosmo.min.css', b'Cosmo'), (b'cyborg.min.css', b'Cyborg'), (b'darkly.min.css', b'Darkly'), (b'flatly.min.css', b'Flatly'), (b'journal.min.css', b'Journal'), (b'lumen.min.css', b'Lumen'), (b'readable.min.css', b'Readable'), (b'simplex.min.css', b'Simplex'), (b'slate.min.css', b'Slate'), (b'spacelab.min.css', b'Spacelab'), (b'superhero.min.css', b'Superhero'), (b'united.min.css', b'United'), (b'yeti.min.css', b'Yeti')])),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', blank=True)),
            ],
            options={
                'ordering': ['email'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
