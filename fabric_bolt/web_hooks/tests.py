"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache

from model_mommy import mommy

from fabric_bolt.projects import models
from fabric_bolt.web_hooks import models as hook_models

User = get_user_model()


class BasicTests(TestCase):

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

    def test_create_url(self):
        c = self.client
        result = c.get(reverse('hooks_hook_create'))
        self.assertIn(result.status_code, [200, 302])

    def test_hook_with_project_url(self):
        c = self.client
        result = c.get(reverse('hooks_hook_create_with_project', args=(self.project.pk,)))
        self.assertIn(result.status_code, [200, 302])

    def test_hook_view(self):
        c = self.client
        result = c.get(reverse('hooks_hook_view', args=(self.project_hook.pk,)))
        self.assertIn(result.status_code, [200, 302])

    def test_hook_update(self):
        c = self.client
        result = c.get(reverse('hooks_hook_update', args=(self.project_hook.pk,)))
        self.assertIn(result.status_code, [200, 302])

    def test_hook_delete(self):
        c = self.client
        result = c.get(reverse('hooks_hook_delete', args=(self.project_hook.pk,)))
        self.assertIn(result.status_code, [200, 302])

    def test_web_hooks(self):

        self.assertEqual(2, self.project.web_hooks().count())

    def test_global_web_hooks(self):
        global_hooks = hook_models.Hook.objects.filter(project=None)

        self.assertEqual(1, global_hooks.count())

    def test_project_web_hooks(self):
        project_hooks = hook_models.Hook.objects.filter(project=self.project)

        self.assertEqual(1, project_hooks.count())