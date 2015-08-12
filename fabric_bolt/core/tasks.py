# coding=utf-8
import json
import subprocess
from django.conf import settings
from fabric_bolt.projects.models import Deployment
from fabric_bolt.projects.util import build_command


try:
    from uwsgidecorators import *
except ImportError:
    def spool(f): return f

@spool
def deploy(args):
    print settings.DATABASES
    deployment = Deployment.objects.get(pk=int(args['deployment_id']))
    deployment.status = Deployment.RUNNING
    deployment.save()
    process = subprocess.Popen(
        build_command(deployment, json.loads(deployment.configuration)),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        executable=getattr(settings, 'SHELL', '/bin/sh'),
    )

    # TODO: Optimize this _if_ needed
    deployment.output = ""
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            if process.returncode == 0:
                deployment.status = Deployment.SUCCESS
            else:
                deployment.status = Deployment.FAILED
            deployment.save()
            break

        deployment.output += nextline
        deployment.save()