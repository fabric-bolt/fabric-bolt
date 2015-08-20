from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from fabric_bolt.projects import models
from fabric_bolt.web_hooks import models as hook_models

from django.forms.models import model_to_dict

User = get_user_model()


class TestHooksViews(TestCase):

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

    def test_hooks_hook_create(self):

        view = reverse('hooks_hook_create')

        get_response = self.client.get(view)

        self.assertEqual(get_response.status_code, 200)

        self.client.post(view, {'url': 'http://www.lookthisup.com/'})

        hooks = hook_models.Hook.objects.filter(url='http://www.lookthisup.com/')

        self.assertTrue(hooks.exists())

    def test_delete_hook_view(self):

        hook_to_delete = hook_models.Hook()
        hook_to_delete.url = 'http://www.deleteme.com/'
        hook_to_delete.save()

        self.assertTrue(hook_to_delete.pk)

        view = reverse('hooks_hook_delete', args=(hook_to_delete.pk,))

        self.client.post(view)

        hooks = hook_models.Hook.objects.filter(url='http://www.deleteme.com/')

        self.assertFalse(hooks.exists())
