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


class TestHooksURLS(TestCase):

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

        project_hook = hook_models.Hook()
        project_hook.url = 'http://example.com/project/hook/'
        project_hook.project = project
        project_hook.save()

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

    def test_hook_reverse(self):
        h = hook_models.Hook()
        h.url = 'http://www.example.com'

        self.assertEqual(reverse('index'), h.get_absolute_url())

    def test_hook_reverse_with_project(self):
        h = hook_models.Hook()
        h.url = 'http://www.example.com'
        h.project = self.project

        self.assertEqual(reverse('projects_project_view', args=(self.project.pk,)), h.get_absolute_url())

    def test_hook_objects_manager(self):

        hooks = hook_models.Hook.objects.hooks(self.project)

        self.assertEqual(self.project_hook, hooks[0])

