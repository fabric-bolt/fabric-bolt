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
from fabric_bolt.projects.util import get_fabfile_path, build_command, parse_task_details

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

        self.deployment = deployment

        self.project = project

    def test_project_crud_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_project_create'))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_project_view', args=(self.project.pk,)))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_project_update', args=(self.project.pk,)))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_project_delete', args=(self.project.pk,)))
        self.assertIn(result.status_code, [200, 302])

    def test_project_configuration_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_configuration_create', args=(self.project.pk,)))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_configuration_stage_create', args=(self.project.pk, self.stage.pk)))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_configuration_update', args=(self.configuration.project_id, self.configuration.pk,)))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_configuration_delete', args=(self.configuration.project_id, self.configuration.pk,)))
        self.assertIn(result.status_code, [200, 302])

    def test_project_deployment_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_deployment_create', args=(self.project.pk, self.stage.pk)) + '?task=bootstrap')
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_deployment_detail', args=(self.project.pk, self.stage.pk, self.deployment.pk,)))
        self.assertIn(result.status_code, [200, 302])

        # result = c.get(reverse('projects_deployment_output', args=(self.deployment.pk,)))
        # self.assertIn(result.status_code, [200, 302])

    def test_project_stage_urls(self):
        """
        Tests that all views return status code of 200
        """
        c = self.client
        result = c.get(reverse('projects_stage_create', args=(self.project.pk, )))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_stage_update', args=(self.project.pk, self.stage.pk)))
        self.assertIn(result.status_code, [200, 302])

        result = c.get(reverse('projects_stage_view', args=(self.project.pk, self.stage.pk)))
        self.assertIn(result.status_code, [200, 302])

    def test_stage_configuration_cram_a_lam(self):
        """Let's make sure our configuration mashing together works as expected"""
        project_configs = [
            {'key': 'number1', 'value': '100'},
            {'key': 'number2', 'value': '200'},
            {'key': 'number3', 'value': '300'},
            {'key': 'number4', 'value': '400'},
        ]

        for config in project_configs:
            c = models.Configuration()
            c.project = self.project
            c.key = config['key']
            c.value = config['value']
            c.save()

        configurations_round_one = self.stage.get_configurations()

        # These should be what we're expecting
        self.assertEqual(configurations_round_one['number1'].get_value(), '100')
        self.assertEqual(configurations_round_one['number2'].get_value(), '200')
        self.assertEqual(configurations_round_one['number3'].get_value(), '300')
        self.assertEqual(configurations_round_one['number4'].get_value(), '400')

        stage_configs = [

            {'key': 'number2', 'value': '5'},
            {'key': 'number3', 'value': '4'},
            {'key': 'number4', 'value': '3'},
        ]

        for config in stage_configs:
            c = models.Configuration()
            c.project = self.project
            c.stage = self.stage
            c.key = config['key']
            c.value = config['value']
            c.save()

        configurations = self.stage.get_configurations()

        # The stage configs take the cake over project configs
        self.assertEqual(configurations['number1'].get_value(), '100')
        self.assertEqual(configurations['number2'].get_value(), '5')
        self.assertEqual(configurations['number3'].get_value(), '4')
        self.assertEqual(configurations['number4'].get_value(), '3')


class UtilTests(TestCase):
    def test_build_command_injection(self):
        deployment = mommy.make(models.Deployment, task__name='test_env')

        cache.delete_many(['project_{}_fabfile_tasks'.format(deployment.stage.project_id),
                   'project_{}_fabfile_path'.format(deployment.stage.project_id)])

        configuration = mommy.make(models.Configuration, key='foo=bar -i /path/to/keyfile --set foo2', value='bar')
        deployment.stage.configuration_set.add(configuration)

        command = build_command(deployment, {})
        fabfile_path, active_loc = get_fabfile_path(deployment.stage.project)

        self.assertEqual(
            command,
            'fab test_env --set "foo\\=bar -i /path/to/keyfile --set foo2=bar" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        configuration = mommy.make(models.Configuration, key='dummy_key', value='dummy_value')
        deployment.stage.configuration_set.add(configuration)

        command = build_command(deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "foo\=bar -i /path/to/keyfile --set foo2=bar,dummy_key=dummy_value" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='dummy_key=test" | ls #', value='dummy_value')
        deployment.stage.configuration_set.add(configuration)

        command = build_command(deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "dummy_key\=test\\" | ls #=dummy_value" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='dummy_key', value='dummy_value,x=y')
        deployment.stage.configuration_set.add(configuration)

        command = build_command(deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "dummy_key=dummy_value\,x\=y" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='dummy_key=blah,x', value='dummy_value')
        deployment.stage.configuration_set.add(configuration)

        command = build_command(deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "dummy_key\=blah\,x=dummy_value" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='key_filename', value='my_ssh_key')
        deployment.stage.configuration_set.add(configuration)

        command = build_command(deployment, {})

        self.assertEqual(
            command,
            'fab test_env -i my_ssh_key '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

    def test_build_command_with_args(self):
        deployment = mommy.make(models.Deployment, task__name='test_env')

        configuration = mommy.make(models.Configuration, key='arg', value='arg_value', task_argument=True,
                                   task_name='test_env')
        deployment.stage.configuration_set.add(configuration)

        command = build_command(deployment, {})
        fabfile_path, active_loc = get_fabfile_path(deployment.stage.project)

        self.assertEqual(
            command,
            'fab test_env:arg="arg_value" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

    def test_parse_task_details(self):
        output = """Displaying detailed information for task 'test_env':

    No docstring provided
    Arguments: arg, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21, arg22, arg23, arg24, arg25, arg26, arg27, arg28, arg29, arg30

"""

        details = parse_task_details('test_env', output)

        self.assertEqual(len(details), 3)
        self.assertEqual(details[0], 'test_env')
        self.assertEqual(details[1], None)
        self.assertListEqual(details[2], ['arg', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6', 'arg7', 'arg8', 'arg9', 'arg10', 'arg11', 'arg12', 'arg13', 'arg14', 'arg15', 'arg16', 'arg17', 'arg18', 'arg19', 'arg20', 'arg21', 'arg22', 'arg23', 'arg24', 'arg25', 'arg26', 'arg27', 'arg28', 'arg29', 'arg30'])

        output = """Displaying detailed information for task 'do_nothing':

    Awesome docstring
    Arguments: test='default'

"""
        details = parse_task_details('do_nothing', output)

        self.assertEqual(len(details), 3)
        self.assertEqual(details[0], 'do_nothing')
        self.assertEqual(details[1], 'Awesome docstring')
        self.assertEqual(len(details[2]), 1)
        self.assertIsInstance(details[2][0], tuple)
        self.assertTupleEqual(details[2][0], ('test', 'default'))

        output = """Displaying detailed information for task 'do_nothing':

    Awesome docstring
    Arguments: test='default', test2

"""
        details = parse_task_details('do_nothing', output)

        self.assertEqual(len(details), 3)
        self.assertEqual(details[0], 'do_nothing')
        self.assertEqual(details[1], 'Awesome docstring')
        self.assertEqual(len(details[2]), 2)
        self.assertIsInstance(details[2][0], tuple)
        self.assertTupleEqual(details[2][0], ('test', 'default'))
        self.assertIsInstance(details[2][1], str)
        self.assertEqual(details[2][1], 'test2')

        output = """Displaying detailed information for task 's':

    Set the Site that we're deploying or bootstrapping. For example s:production
    :param site_alias:
    :return:

    Arguments: site_alias

"""
        details = parse_task_details('s', output)

        self.assertEqual(len(details), 3)
        self.assertEqual(details[0], 's')
        self.assertEqual(details[1], "Set the Site that we're deploying or bootstrapping. For example s:production\n:param site_alias:\n:return:")
        self.assertEqual(len(details[2]), 1)
        self.assertIsInstance(details[2][0], str)
        self.assertEqual(details[2][0], 'site_alias')

        output = """Displaying detailed information for task 'deploy':

    Pulls code, updates pip, syncs, migrates, collects static, resets permissions and reloads supervisor and nginx
    :param hard:
    :return:

    Arguments: hard=False

"""
        details = parse_task_details('deploy', output)

        self.assertEqual(len(details), 3)
        self.assertEqual(details[0], 'deploy')
        self.assertEqual(details[1], "Pulls code, updates pip, syncs, migrates, collects static, resets permissions and reloads supervisor and nginx\n:param hard:\n:return:")
        self.assertEqual(len(details[2]), 1)
        self.assertIsInstance(details[2][0], str)
        self.assertEqual(details[2][0], 'hard')