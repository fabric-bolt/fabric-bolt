import logging
import sys
import subprocess
from threading import Thread
import time
import fcntl
import os

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from views import get_fabfile_path, fabric_special_options
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

    def build_command(self):
        command = ['fab', self.deployment.task.name]

        hosts = self.deployment.stage.hosts.values_list('name', flat=True)
        if hosts:
            command.append('--hosts=' + ','.join(hosts))

        # Get the dictionary of configurations for this stage
        config = self.deployment.stage.get_configurations()

        config.update(self.request.session.get('configuration_values', {}))

        command_to_config = {x.replace('-', '_'): x for x in fabric_special_options}

        # Take the special env variables out
        normal_options = list(set(config.keys()) - set(command_to_config.keys()))

        # Special ones get set a different way
        special_options = list(set(config.keys()) & set(command_to_config.keys()))

        def get_key_value_string(key, value):
            if isinstance(value, bool):
                return key + ('' if value else '=')
            elif isinstance(value, float):
                return key + '=' + str(value)
            else:
                return '{}="{}"'.format(key, value.replace('"', '\\"'))

        if normal_options:
            command.append('--set ' + ','.join(get_key_value_string(key, config[key]) for key in normal_options))

        if special_options:
            for key in special_options:
                command.append('--' + get_key_value_string(command_to_config[key], config[key]))

        command.append('--fabfile={}'.format(get_fabfile_path(self.deployment.stage.project)))

        return command

    def output_stream_generator(self, *args, **kwargs):
        self.process = subprocess.Popen(self.build_command(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

        fd = self.process.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        all_output = ''
        while True:
            try:
                nextline = self.process.stdout.read()
            except IOError:
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
