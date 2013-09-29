"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse

from django.test import TestCase

from . import models

from django.contrib.auth import get_user_model

User = get_user_model()


class SimpleTest(TestCase):

    project_type = None
    project = None
    stage = None
    configuration = None
    task = None
    deployment = None

    def setUp(self):
        password = 'mypassword'

        self.user = User.objects.create_superuser('myemail@test.com', password)

        # You'll need to log him in before you can send requests through the client
        self.client.login(email=self.user.email, password=password)

        self._create_project()

    def _create_project(self):

        # Bare bones project type
        project_type = models.ProjectType()
        project_type.name = 'Django'
        self.project_type = project_type.save()

        # Bare bones project
        project = models.Project()
        project.name = 'TEST_PROJECT'
        project.type = project_type
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

        self.deployment = deployment

        self.project = project

    def test_project_crud_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_project_create'))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_project_view', args=(self.project.pk,)))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_project_update', args=(self.project.pk,)))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_project_delete', args=(self.project.pk,)))
        self.assertEqual(result.status_code, 200)

    def test_project_configuration_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_configuration_create', args=(self.project.pk,)))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_configuration_stage_create', args=(self.project.pk, self.stage.pk)))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_configuration_update', args=(self.configuration.pk,)))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_configuration_delete', args=(self.configuration.pk,)))
        self.assertEqual(result.status_code, 200)

    def test_project_deployment_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_deployment_create', args=(self.stage.pk, 'bootstrap')))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_deployment_detail', args=(self.deployment.pk,)))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_deployment_output', args=(self.deployment.pk,)))
        self.assertEqual(result.status_code, 200)

    def test_project_stage_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_stage_create', args=(self.project.pk, )))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_stage_update', args=(self.project.pk, self.stage.pk)))
        self.assertEqual(result.status_code, 200)

        result = c.get(reverse('projects_stage_view', args=(self.project.pk, self.stage.pk)))
        self.assertEqual(result.status_code, 200)