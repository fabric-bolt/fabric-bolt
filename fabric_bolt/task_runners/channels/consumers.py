import json
import os
import subprocess
from importlib import import_module

import ansiconv
import sys

import fcntl
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
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
        stdin=subprocess.PIPE,
        shell=True,
        executable=getattr(settings, 'SHELL', '/bin/sh'),
        close_fds=True
    )

    fd = process.stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    while True:
        try:
            nextline = process.stdout.readline()
        except IOError as e:
            nextline = ''

        if nextline == '' and process.poll() is not None:
            break
        #
        # next_input = deployment.get_next_input()
        # if next_input:
        #     process.stdin.write(next_input + '\n')

        if nextline:
            Group("deployment-{}".format(deployment.id)).send({
                "text": json.dumps({
                    'status': 'pending',
                    'text': str('<span class="output-line">{}</span>'.format(ansiconv.to_html(nextline)))
                }),
            }, immediately=True)

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
    }, immediately=True)

    deployment_finished.send(deployment, deployment_id=deployment.pk)


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})

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
    }, immediately=True)


# @channel_session
# def ws_receive(message):
#     deployment = Deployment.objects.filter(pk=message.channel_session['deployment_id'])[0]
#     deployment.add_input(message.content['text'])


@channel_session_user
def ws_disconnect(message):
    Group("deployment-{}".format(message.channel_session['deployment_id'])).discard(message.reply_channel)
