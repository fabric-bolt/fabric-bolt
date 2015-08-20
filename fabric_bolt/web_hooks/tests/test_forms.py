"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from fabric_bolt.projects import models
from fabric_bolt.web_hooks import models as hook_models
from fabric_bolt.web_hooks import forms

User = get_user_model()


class TestHooksForms(TestCase):

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

    def test_hook_create_form(self):
        hook_form = forms.HookCreateForm(data={'project': self.project.pk, 'url': 'http://www.example.com'})
        hook_form.save()

    def test_hook_create_form_clean_project(self):
        hook_form = forms.HookCreateForm(data={'project': self.project.pk, 'url': 'http://www.example.com'})

        hook_form.cleaned_data = { 'project': self.project.pk}
        p = hook_form.clean_project()

        self.assertEqual(self.project.pk, p.pk)

    def test_hook_create_form_clean_project_none(self):
        hook_form = forms.HookCreateForm(data={'project': self.project.pk, 'url': 'http://www.example.com'})

        hook_form.cleaned_data = { 'project': None}
        p = hook_form.clean_project()

        self.assertEqual(p, None)

    def test_hook_update_form(self):
        hook_form = forms.HookUpdateForm(instance=self.project, data={'project': self.project.pk, 'url': 'http://www.example.com'})
        hook_form.is_valid()
        hook_form.save()
