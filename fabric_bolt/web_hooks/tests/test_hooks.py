"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

from model_mommy import mommy

from fabric_bolt.projects import models
from fabric_bolt.web_hooks import models as hook_models
from fabric_bolt.web_hooks.tasks import DeliverHook

import mock

User = get_user_model()


class TestHooks(TestCase):

    project_type = None
    project = None
    stage = None
    configuration = None
    task = None
    deployment = None

    def setUp(self):
        password = 'mypassword'

        self.user = User.objects.create_superuser(email='myemail@test.com', password=password)

        # You'll need to log him in before you can send requests through the client
        self.client.login(email=self.user.email, password=password)

        self._create_project()

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
        task.name = 'TASK_NAME'
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

        # Setup Hook
        hook = hook_models.Hook()
        hook.url = 'http://example.com'
        hook.save()

        project_hook = hook_models.Hook()
        project_hook.url = 'http://example.com/project/hook/'
        project_hook.project = project
        project_hook.save()

        self.deployment = deployment

        self.hook = hook
        self.project_hook = project_hook

        self.project = project

    def test_web_hooks(self):

        self.assertEqual(2, self.project.web_hooks().count())

    def test_global_web_hooks(self):
        global_hooks = hook_models.Hook.objects.filter(project=None)

        self.assertEqual(1, global_hooks.count())

    def test_project_web_hooks(self):
        project_hooks = hook_models.Hook.objects.filter(project=self.project)

        self.assertEqual(1, project_hooks.count())

    @mock.patch('fabric_bolt.web_hooks.tasks.requests')
    def test_task_post_data(self, mock_requests):

        mock_requests.post.return_value.status_code = 200

        d = DeliverHook()
        ret = d.post_data('http://www.example.com', {'junk': 'payload'})

        self.assertEqual(ret.status_code, 200)

    # def test_task_post_data_run(self):
    #
    #     d = DeliverHook()
    #     ret = d.run('http://www.example.com', {'junk': 'payload'})

    @mock.patch('fabric_bolt.web_hooks.tasks.requests')
    def test_task_delete_hook_410(self, mock_requests):

        # post_data deletes hooks when the status code is 410
        mock_requests.post.return_value.status_code = 410

        h = hook_models.Hook()
        h.url = 'http://example.com/project/delete/me/'
        h.project = self.project
        h.save()

        hook_id = h.pk

        d = DeliverHook()
        ret = d.post_data('http://example.com/api/123', {'junk': 'payload'}, hook_id)

        def look_up_error(hook_id):
            hook_models.Hook.objects.get(pk=hook_id)

        self.assertRaises(hook_models.Hook.DoesNotExist, look_up_error, hook_id)

    @mock.patch('fabric_bolt.web_hooks.tasks.requests')
    def test_task_delete_hook(self, mock_requests):

        # post_data deletes hooks when the status code is 410
        mock_requests.post.return_value.status_code = 410

        h = hook_models.Hook()
        h.url = 'http://example.com/project/delete/me/'
        h.project = self.project
        h.save()

        d = DeliverHook()

        # We're testing we don't have hook deleted, since we're not passing in the hook id
        ret = d.post_data('http://example.com/api/123', {'junk': 'payload'})

        hook_models.Hook.objects.get(pk=h.pk)

    # @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    #                    CELERY_ALWAYS_EAGER=True,
    #                    BROKER_BACKEND='memory')
    # def test_task_wrapper(self):
    #     from fabric_bolt.web_hooks.tasks import deliver_hook_wrapper
    #
    #     deliver_hook_wrapper('http://www.example.com', {'dummy': 'payload'})

