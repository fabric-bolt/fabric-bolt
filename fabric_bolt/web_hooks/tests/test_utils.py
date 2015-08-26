"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

from fabric_bolt.projects import models
from fabric_bolt.web_hooks import models as hook_models
from fabric_bolt.web_hooks import forms
from fabric_bolt.web_hooks import receivers
from fabric_bolt.web_hooks import utils

import mock

User = get_user_model()


def custom_serializer(*args, **kwargs):
    return 'CUSTOM_SERIALIZER_CALLED'


def custom_deliverer(*args, **kwargs):
    return 'CUSTOM_HOOK_DELIVERER'


class CustomError(Exception):
    pass


def custom_payload_generator(*args, **kwargs):
    raise CustomError('Error Raised')


class TestHooksUtils(TestCase):

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

        self.deployment = deployment
        self.project = project

    def test_hook_serialize_hook(self):
        class TestClass(object):
            def serialize_hook(self, hook):
                return 'RETURNED'

        test_class = TestClass()
        self.assertEqual(utils.serialize_hook(test_class), 'RETURNED')

    def test_serialize_hook_no_serialize_hook_method(self):

        def dict():
            return 'DICT_TEST'

        test_class = hook_models.Hook()
        test_class.dict = dict
        # self.fail(utils.serialize_hook(test_class))
        self.assertEqual(utils.serialize_hook(test_class)['hook'], 'DICT_TEST')

    def test_receivers_no_hooks(self):

        s = models.Stage()
        s.project = self.project
        s.name = 'NEW_STAGE'
        s.save()

        p = self.deployment
        p.pk = None
        p.stage = s
        p.save()

        ret = receivers.web_hook_receiver(None, deployment_id=p.pk)
        self.assertEqual(ret, None)

    @override_settings(HOOK_DELIVERER='fabric_bolt.web_hooks.tests.test_utils.custom_deliverer')
    def test_receivers_no_hooks(self):

        s = models.Stage()
        s.project = self.project
        s.name = 'NEW_STAGE'
        s.save()

        p = self.deployment
        p.pk = None
        p.stage = s
        p.save()

        ret = receivers.web_hook_receiver(None, deployment_id=p.pk)
        self.assertEqual(ret, None)


class TestWithHooks(TestCase):

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

    @override_settings(HOOK_SERIALIZER='fabric_bolt.web_hooks.tests.test_utils.custom_serializer')
    def test_custom_serializer(self):

        test_class = hook_models.Hook()
        test_class.dict = dict

        ret = utils.serialize_hook(test_class)

        self.assertEqual(ret, 'CUSTOM_SERIALIZER_CALLED')

    def test_get_module(self):
        s = utils.get_module('django.template.defaultfilters.slugify')

        from django.template.defaultfilters import slugify

        self.assertEqual(s, slugify)

    def test_get_module_error(self):

        def lookup():

            utils.get_module('junk.path.error')

        self.assertRaises(ImportError, lookup)

    def test_get_module_error_junk(self):

        def lookup():

            utils.get_module('django.template.defaultfilters.junkify')

        self.assertRaises(ImportError, lookup)

    @override_settings(HOOK_DELIVERER='fabric_bolt.web_hooks.tests.test_utils.custom_deliverer')
    def test_deliver_hook(self):

        def dict():
            return 'DICT_TEST'

        h = hook_models.Hook()
        h.dict = dict

        h.url = 'http://www.example.com'
        receivers.deliver_hook(h, 'http://www.example.com')
