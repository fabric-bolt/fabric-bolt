import logging
import sys
import subprocess
from threading import Thread
import time
import fcntl
import os

from django.conf import settings

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from fabric_bolt.projects.models import Deployment


@namespace('/deployment')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def initialize(self):
        self.logger = logging.getLogger("socketio.deployment")
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, deployment_id):
        self.deployment = Deployment.objects.get(pk=deployment_id)
        if self.deployment.status != self.deployment.PENDING:
            return True

        update_thread = Thread(target=self.output_stream_generator, args=(self,))
        update_thread.daemon = True
        update_thread.start()

        return True

    def on_input(self, text):
        self.process.stdin.write(text + '\n')

        return True

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        self.disconnect(silent=True)
        return True

    def output_stream_generator(self, *args, **kwargs):
        from fabric_bolt.task_runners import backend

        self.process = subprocess.Popen(
            backend.build_command(self.deployment.stage.project, self.deployment, self.request.session, False),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=True,
            executable=getattr(settings, 'SHELL', '/bin/sh'),
            close_fds=True,
        )

        fd = self.process.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        all_output = ''
        while True:
            try:
                nextline = self.process.stdout.read()
            except IOError as e:
                print e
                nextline = ''

            if nextline == '' and self.process.poll() != None:
                break

            all_output += nextline

            if nextline:
                self.broadcast_event('output', {'status': 'pending', 'lines': str(nextline)})
            time.sleep(0.00001)

            sys.stdout.flush()

        self.deployment.status = self.deployment.SUCCESS if self.process.returncode == 0 else self.deployment.FAILED

        self.deployment.output = all_output
        self.deployment.save()

        self.broadcast_event('output', {'status': self.deployment.status})

        self.disconnect()
