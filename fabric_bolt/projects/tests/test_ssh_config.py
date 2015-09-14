from django.test import TestCase
from django.contrib.auth import get_user_model

from fabric_bolt.hosts.utils import create_ssh_config
from fabric_bolt.projects import models
from fabric_bolt.task_runners import backend

User = get_user_model()


class SSHConfigTests(TestCase):

    project_type = None
    project = None
    stage = None
    configuration = None
    task = None
    deployment = None
    ssh_config = None

    def setUp(self):
        password = 'mypassword'

        self.user = User.objects.create_superuser(email='myemail@test.com', password=password)

        # You'll need to log him in before you can send requests through the client
        self.client.login(email=self.user.email, password=password)

        self._create_project()
        self._create_ssh_config()

    def _create_ssh_config(self):

        self.ssh_config = create_ssh_config()

    def _create_project(self):
        # Bare bones project
        project = models.Project()
        project.name = 'TEST_PROJECT'
        project.description = 'TEST_DESCRIPTION'

        project.save()

        # Bare bones stage
        stage = models.Stage()
        stage.project = project
        stage.name = 'Production'
        stage.save()

        self.stage = stage

        # Bare bones configuration
        configuration = models.Configuration()
        configuration.project = project
        configuration.stage = stage
        configuration.key = 'KEY'
        configuration.value = 'VALUE'
        configuration.prompt_me_for_input = True
        configuration.save()

        self.configuration = configuration

        # Bare bones task
        task = models.Task()
        task.name = 'update_sandbox_site'
        task.save()

        self.task = task

        # Bare bones deployment
        deployment = models.Deployment()
        deployment.user = self.user
        deployment.stage = stage
        deployment.comments = 'COMMENTS'
        deployment.output = 'OUTPUT'
        deployment.task = task
        deployment.save()

        self.deployment = deployment

        self.project = project

    def test_create_ssh_config(self):
        ssh_config = create_ssh_config(remote_user='test_user')

        self.assertEquals('test_user', ssh_config.remote_user)

    def test_command_with_ssh_config(self):

        command = backend.build_command(self.project, self.deployment, {})

        fabfile_path, active_loc = backend.get_fabfile_path(self.deployment.stage.project)

        self.assertEqual(
            command,
            'fab update_sandbox_site --set "KEY=VALUE" '
            '--abort-on-prompts -i {} '.format(self.ssh_config.private_key_file._get_path()) +
            '-u {} --fabfile={}'.format(self.ssh_config.remote_user, fabfile_path)
        )
