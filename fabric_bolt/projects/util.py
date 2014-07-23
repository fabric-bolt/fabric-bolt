import os
import re
import subprocess

from django.utils.text import slugify
from django.conf import settings
from django.contrib import messages

from virtualenv import create_environment

# These options are passed to Fabric as: fab task --abort-on-prompts=True --user=root ...
fabric_special_options = ['no_agent', 'forward-agent', 'config', 'disable-known-hosts', 'keepalive',
                          'password', 'parallel', 'no-pty', 'reject-unknown-hosts', 'skip-bad-hosts', 'timeout',
                          'command-timeout', 'user', 'warn-only', 'pool-size']


def check_output_with_ssh_key(command):
    if getattr(settings, 'GIT_SSH_KEY_LOCATION', None):
        return subprocess.check_output(
            'ssh-agent bash -c "ssh-add {};{}"'.format(settings.GIT_SSH_KEY_LOCATION, command),
            shell=True
        )
    else:
        out = subprocess.check_output([command], shell=True)
        return out


def update_project_git(project, cache_dir, repo_dir):
    if not os.path.exists(repo_dir):
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        check_output_with_ssh_key('git clone {} {}'.format(project.repo_url, repo_dir))
    else:
        check_output_with_ssh_key(
            'cd {0};git stash;git pull'.format(repo_dir)
        )


def setup_virtual_env_if_needed(repo_dir):
    env_dir = os.path.join(repo_dir, 'env')
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
        create_environment(env_dir)


def update_project_requirements(project, repo_dir, activate_loc):
    pip_installs = ' '.join(project.fabfile_requirements.splitlines())

    check_output_with_ssh_key('source {} && cd {};pip install {}'.format(activate_loc, repo_dir, pip_installs))


def get_fabfile_path(project):
    if project.use_repo_fabfile:
        cache_dir = os.path.join(settings.PUBLIC_DIR, '.repo_caches')
        repo_dir = os.path.join(cache_dir, slugify(project.name))

        update_project_git(project, cache_dir, repo_dir)
        setup_virtual_env_if_needed(repo_dir)
        activate_loc = os.path.join(repo_dir, 'env', 'bin', 'activate')

        update_project_requirements(project, repo_dir, activate_loc)

        return os.path.join(repo_dir, 'fabfile.py'), activate_loc
    else:
        return settings.FABFILE_PATH, None


def get_fabric_tasks(request, project):
    """
    Generate a list of fabric tasks that are available
    """
    try:
        fabfile_path, activate_loc = get_fabfile_path(project)

        if activate_loc:
            output = subprocess.check_output('source {};fab --list --fabfile={}'.format(activate_loc, fabfile_path), shell=True)
        else:
            output = subprocess.check_output(['fab', '--list', '--fabfile={}'.format(fabfile_path)])

        lines = output.splitlines()[2:]
        dict_with_docs = {}
        for line in lines:
            match = re.match(r'^\s*([^\s]+)\s*(.*)$', line)
            if match:
                name, desc = match.group(1), match.group(2)
                if desc.endswith('...'):
                    if activate_loc:
                        o = subprocess.check_output(
                            'source {};fab --display={} --fabfile={}'.format(activate_loc, name, fabfile_path),
                            shell=True
                        )
                    else:
                        o = subprocess.check_output(
                            ['fab', '--display={}'.format(name), '--fabfile={}'.format(fabfile_path)]
                        )
                    try:
                        desc = o.splitlines()[2].strip()
                    except:
                        pass # just stick with the original truncated description
                dict_with_docs[name] = desc
    except Exception as e:
        messages.error(request, 'Error loading fabfile: ' + str(e))
        dict_with_docs = {}
    return dict_with_docs


def clean_key_string(key):
    key = key.replace('"', '\\"')  # escape double quotes
    key = key.replace('=', '')  # remove = because that would be setting a new key

    return key


def clean_value_string(value):
    value = value.replace('"', '\\"')  # escape double quotes

    return value


def get_key_value_string(key, value):
    key = clean_key_string(key)

    if isinstance(value, bool):
        return key + ('' if value else '=')
    elif isinstance(value, float):
        return key + '=' + str(value)
    else:
        return '{}={}'.format(key, clean_value_string(value))


def build_command(deployment, session, abort_on_prompts=True):
    command = ['fab', deployment.task.name]

    if abort_on_prompts:
        command.append('--abort-on-prompts')

    hosts = deployment.stage.hosts.values_list('name', flat=True)
    if hosts:
        command.append('--hosts=' + ','.join(hosts))

    # Get the dictionary of configurations for this stage
    config = deployment.stage.get_configurations()

    config.update(session.get('configuration_values', {}))

    command_to_config = {x.replace('-', '_'): x for x in fabric_special_options}

    # Take the special env variables out
    normal_options = list(set(config.keys()) - set(command_to_config.keys()))

    # Special ones get set a different way
    special_options = list(set(config.keys()) & set(command_to_config.keys()))

    if normal_options:
        command.append('--set')
        command.append('"' + ','.join(get_key_value_string(key, config[key]) for key in normal_options) + '"')

    if special_options:
        for key in special_options:
            command.append('--' + get_key_value_string(command_to_config[key], config[key]))

    fabfile_path, active_loc = get_fabfile_path(deployment.stage.project)
    command.append('--fabfile={}'.format(fabfile_path))

    if active_loc:
        return 'source {};'.format(active_loc) + ' '.join(command)
    else:
        return ' '.join(command)