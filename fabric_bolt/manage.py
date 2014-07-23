#!/usr/bin/env python
import os, sys

# Adds the fabric_bolt package from the working copy instead of site_packages
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    from django.conf import settings

    if getattr(settings, 'SOCKETIO_ENABLED', False):
        from gevent import monkey
        monkey.patch_all()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabric_bolt.core.settings.local')
    sys.path.append(os.getcwd())

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
