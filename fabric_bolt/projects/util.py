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
    key = key.replace(',', '\,')  # escape commas, that would be adding a new value
    key = key.replace('=', '\=')  # escape = because that would be setting a new key

    return key


def clean_value_string(value):
    value = value.replace('"', '\\"')  # escape double quotes
    value = value.replace(',', '\,')  # escape commas, that would be adding a new value
    value = value.replace('=', '\=')  # escape = because that would be setting a new key

    return value


def clean_arg_key_string(key):
    # this has to be a valid python function argument, so we can get pretty strict here
    key = re.sub(r'[^0-9a-zA-Z_]', '', key)  # remove anything that isn't a number, letter, or underscore

    return key


def get_key_value_string(key, config):
    key = clean_key_string(key)

    if config.data_type == config.BOOLEAN_TYPE:
        return key + ('' if config.get_value() else '=')
    elif config.data_type == config.NUMBER_TYPE:
        return key + '=' + str(config.get_value())
    else:
        return '{}={}'.format(key, clean_value_string(config.get_value()))


def update_config_values_from_session(configs, session):
    configs = configs.copy()

    for key, config in configs.iteritems():
        if session.get('configuration_values', {}).get(key, None) is not None:
            config.set_value(session['configuration_values'][key])

    return configs


def build_command(deployment, session, abort_on_prompts=True):
    # Get the dictionary of configurations for this stage
    configs = deployment.stage.get_configurations()
    configs = update_config_values_from_session(configs, session)

    task_args = [key for key, config in configs.iteritems() if config.task_argument]
    task_configs = [key for key, config in configs.iteritems() if not config.task_argument]

    command_to_config = {x.replace('-', '_'): x for x in fabric_special_options}

    # Take the special env variables out
    normal_task_configs = list(set(task_configs) - set(command_to_config.keys()))

    # Special ones get set a different way
    special_task_configs = list(set(task_configs) & set(command_to_config.keys()))

    command = 'fab ' + deployment.task.name

    if task_args:
        command += ':'
        command += ','.join('{}="{}"'.format(clean_arg_key_string(key), clean_value_string(unicode(configs[key].get_value()))) for key in task_args)

    if normal_task_configs:
        command += ' --set '
        command += '"' + ','.join(get_key_value_string(key, configs[key]) for key in normal_task_configs) + '"'

    if special_task_configs:
        for key in special_task_configs:
            command += ' --' + get_key_value_string(command_to_config[key], configs[key])

    if abort_on_prompts:
        command += ' --abort-on-prompts'

    hosts = deployment.stage.hosts.values_list('name', flat=True)
    if hosts:
        command += ' --hosts=' + ','.join(hosts)

    fabfile_path, active_loc = get_fabfile_path(deployment.stage.project)
    command += ' --fabfile={}'.format(fabfile_path)

    if active_loc:
        return 'source {};'.format(active_loc) + ' ' + command
    else:
        return command