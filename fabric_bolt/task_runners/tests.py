"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache

from model_mommy import mommy

from fabric_bolt.projects import models

from . import backend

User = get_user_model()


class BackendTests(TestCase):
    def test_build_command_injection(self):
        deployment = mommy.make(models.Deployment, task__name='test_env')

        cache.delete_many(['project_{}_fabfile_tasks'.format(deployment.stage.project_id),
                   'project_{}_fabfile_path'.format(deployment.stage.project_id)])

        configuration = mommy.make(models.Configuration, key='foo=bar -i /path/to/keyfile --set foo2', value='bar')
        deployment.stage.configuration_set.add(configuration)

        command = backend.build_command(deployment.stage.project, deployment, {})
        fabfile_path, active_loc = backend.get_fabfile_path(deployment.stage.project)

        self.assertEqual(
            command,
            'fab test_env --set "foo\\=bar -i /path/to/keyfile --set foo2=bar" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        configuration = mommy.make(models.Configuration, key='dummy_key', value='dummy_value')
        deployment.stage.configuration_set.add(configuration)

        command = backend.build_command(deployment.stage.project, deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "foo\=bar -i /path/to/keyfile --set foo2=bar,dummy_key=dummy_value" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='dummy_key=test" | ls #', value='dummy_value')
        deployment.stage.configuration_set.add(configuration)

        command = backend.build_command(deployment.stage.project, deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "dummy_key\=test\\" | ls #=dummy_value" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='dummy_key', value='dummy_value,x=y')
        deployment.stage.configuration_set.add(configuration)

        command = backend.build_command(deployment.stage.project, deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "dummy_key=dummy_value\,x\=y" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='dummy_key=blah,x', value='dummy_value')
        deployment.stage.configuration_set.add(configuration)

        command = backend.build_command(deployment.stage.project, deployment, {})

        self.assertEqual(
            command,
            'fab test_env --set "dummy_key\=blah\,x=dummy_value" '
            '--abort-on-prompts --fabfile={}'.format(fabfile_path)
        )

        deployment.stage.configuration_set.clear()
        configuration = mommy.make(models.Configuration, key='key_filename', value='my_ssh_key')
        deployment.stage.configuration_set.add(configuration)

        command = backend.build_command(deployment.stage.project, deployment, {})

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

        command = backend.build_command(deployment.stage.project, deployment, {})
        fabfile_path, active_loc = backend.get_fabfile_path(deployment.stage.project)

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

        details = backend.parse_task_details('test_env', output)

        self.assertEqual(len(details), 3)
        self.assertEqual(details[0], 'test_env')
        self.assertEqual(details[1], None)
        self.assertListEqual(details[2], ['arg', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6', 'arg7', 'arg8', 'arg9', 'arg10', 'arg11', 'arg12', 'arg13', 'arg14', 'arg15', 'arg16', 'arg17', 'arg18', 'arg19', 'arg20', 'arg21', 'arg22', 'arg23', 'arg24', 'arg25', 'arg26', 'arg27', 'arg28', 'arg29', 'arg30'])

        output = """Displaying detailed information for task 'do_nothing':

    Awesome docstring
    Arguments: test='default'

"""
        details = backend.parse_task_details('do_nothing', output)

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
        details = backend.parse_task_details('do_nothing', output)

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
        details = backend.parse_task_details('s', output)

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
        details = backend.parse_task_details('deploy', output)

        self.assertEqual(len(details), 3)
        self.assertEqual(details[0], 'deploy')
        self.assertEqual(details[1], "Pulls code, updates pip, syncs, migrates, collects static, resets permissions and reloads supervisor and nginx\n:param hard:\n:return:")
        self.assertEqual(len(details[2]), 1)
        self.assertIsInstance(details[2][0], str)
        self.assertEqual(details[2][0], 'hard')