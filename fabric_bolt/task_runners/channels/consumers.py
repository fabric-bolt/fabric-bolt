import json
import subprocess
from importlib import import_module

import ansiconv
import sys

from channels import Group
from channels.auth import channel_session_user_from_http
from channels.sessions import channel_session
from django.conf import settings

from fabric_bolt.projects.models import Project, Deployment
from fabric_bolt.projects.signals import deployment_finished

from .. import backend

import time


def start_task(message):
    time.sleep(1)
    project = Project.objects.get(id=message.content['project_id'])
    deployment = Deployment.objects.get(id=message.content['deployment_id'])
    deployment.output = ''
    deployment.save()

    engine = import_module(settings.SESSION_ENGINE)
    SessionStore = engine.SessionStore
    session = SessionStore(message.content['session_key'])

    if backend.get_task_details(project, deployment.task.name) is None:
        return

    process = subprocess.Popen(
        backend.build_command(project, deployment, session),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        executable=getattr(settings, 'SHELL', '/bin/sh'),
    )

    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break

        Group("deployment-{}".format(deployment.id)).send({
            "text": json.dumps({
                'status': 'pending',
                'text': str('<span class="output-line">{}</span>'.format(ansiconv.to_html(nextline)))
            }),
        })

        deployment.add_output(nextline)

        sys.stdout.flush()

    Deployment.objects.filter(pk=deployment.id).update(
        status=deployment.SUCCESS if process.returncode == 0 else deployment.FAILED
    )

    Group("deployment-{}".format(deployment.id)).send({
        "text": json.dumps({
            'status': deployment.SUCCESS if process.returncode == 0 else deployment.FAILED,
            'text': ''
        }),
    })

    deployment_finished.send(deployment, deployment_id=deployment.pk)


# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    # Work out room name from path (ignore slashes)
    deployment_id = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['deployment_id'] = deployment_id
    Group("deployment-{}".format(deployment_id)).add(message.reply_channel)

    deployment = Deployment.objects.filter(pk=deployment_id)[0]
    Group("deployment-{}".format(deployment_id)).send({
        "text": json.dumps({
            "text": deployment.get_formatted_output(),
            'status': deployment.status
        })
    })


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("deployment-{}".format(message.channel_session['deployment_id'])).discard(message.reply_channel)


# Connected to websocket.connect
@channel_session_user_from_http
def ws_receive(message):
    deployment = Deployment.objects.filter(pk=message.channel_session['deployment_id'])[0]
    deployment.add_input(message.content)
