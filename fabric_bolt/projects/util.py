import os
import re
import subprocess

from django.utils.text import slugify
from django.conf import settings
from django.core.cache import cache

# These options are passed to Fabric as: fab task --abort-on-prompts=True --user=root ...
fabric_special_options = ['no_agent', 'forward-agent', 'config', 'disable-known-hosts', 'keepalive',
                          'password', 'parallel', 'no-pty', 'reject-unknown-hosts', 'skip-bad-hosts', 'timeout',
                          'command-timeout', 'user', 'warn-only', 'pool-size', 'key_filename']


def check_output(command, shell=False):
    executable = None
    if shell:
        executable = getattr(settings, 'SHELL', '/bin/sh')
    return subprocess.check_output(command, shell=shell, executable=executable)


def check_output_with_ssh_key(command):
    if getattr(settings, 'GIT_SSH_KEY_LOCATION', None):
        return check_output('ssh-agent bash -c "ssh-add {};{}"'.format(settings.GIT_SSH_KEY_LOCATION, command),
                            shell=True)
    else:
        return check_output([command], shell=True)


def update_project_git(project, cache_dir, repo_dir):
    if not os.path.exists(repo_dir):
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        check_output_with_ssh_key('git clone {} {}'.format(project.repo_url, repo_dir))
    else:
        check_output_with_ssh_key(
            'cd {0};git stash;git pull'.format(repo_dir)
        )


def setup_link_env_if_needed(repo_dir):
    env_dir = os.path.join(repo_dir, 'env')
    if not os.path.exists(env_dir):
        os.symlink(os.environ.get('VIRTUAL_ENV'), env_dir)


def setup_virtual_env_if_needed(repo_dir):
    env_dir = os.path.join(repo_dir, 'env')
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
        check_output("virtualenv {}".format(env_dir), shell=True)


def update_project_requirements(project, repo_dir, activate_loc):
    pip_installs = ' '.join(project.fabfile_requirements.splitlines())

    check_output_with_ssh_key('source {} && cd {};pip install {}'.format(activate_loc, repo_dir, pip_installs))


def get_fabfile_path(project):
    if project.use_repo_fabfile:
        cache_key = 'project_{}_fabfile_path'.format(project.pk)
        cached_result = cache.get(cache_key)

        if cached_result:
            return cached_result

        cache_dir = os.path.join(settings.PUBLIC_DIR, '.repo_caches')
        repo_dir = os.path.join(cache_dir, slugify(project.name))

        update_project_git(project, cache_dir, repo_dir)
        if project.link_repo_env:
            setup_link_env_if_needed(repo_dir)
        else:
            setup_virtual_env_if_needed(repo_dir)
        activate_loc = os.path.join(repo_dir, 'env', 'bin', 'activate')

        update_project_requirements(project, repo_dir, activate_loc)

        result = os.path.join(repo_dir, 'fabfile.py'), activate_loc
        cache.set(cache_key, result, settings.FABRIC_TASK_CACHE_TIMEOUT)
        return result
    else:
        return settings.FABFILE_PATH, None


def parse_task_details(name, task_output):
    lines = task_output.splitlines()
    docstring = '\n'.join([line.strip() for line in lines[2:-2]]).strip()
    arguments_line = lines[-2].strip()

    if docstring == 'No docstring provided':
        docstring = None

    arguments_line = arguments_line[11:].strip()

    arguments = []

    if arguments_line:
        for arg in arguments_line.split(', '):
            m = re.match(r"^([^=]+)(=(\'?)([^']*)\3)?$", arg)

            if m.group(2):  # found argument with default value
                if m.group(3) == "'":  # default value is a string
                    arguments.append((m.group(1), m.group(4)))
                else:  # found an argument with some other default value.
                    # all fab arguments are translated to strings, so this doesnt make sense. Ignore the default.
                    arguments.append(m.group(1))
            else:
                arguments.append(m.group(1))

    return name, docstring, arguments


def get_fabric_tasks(project):
    """
    Generate a list of fabric tasks that are available
    """

    cache_key = 'project_{}_fabfile_tasks'.format(project.pk)
    cached_result = cache.get(cache_key)

    if cached_result:
        return cached_result

    try:
        fabfile_path, activate_loc = get_fabfile_path(project)

        if activate_loc:
            output = check_output('source {};fab --list --list-format=short --fabfile={}'.format(activate_loc, fabfile_path), shell=True)
        else:
            output = check_output(['fab', '--list', '--list-format=short', '--fabfile={}'.format(fabfile_path)])

        lines = output.splitlines()
        tasks = []
        for line in lines:
            name = line.strip()
            if activate_loc:
                o = check_output(
                    'source {};fab --display={} --fabfile={}'.format(activate_loc, name, fabfile_path),
                    shell=True
                )
            else:
                o = check_output(
                    ['fab', '--display={}'.format(name), '--fabfile={}'.format(fabfile_path)]
                )

            tasks.append(parse_task_details(name, o))

        cache.set(cache_key, tasks, settings.FABRIC_TASK_CACHE_TIMEOUT)
    except Exception as e:
        tasks = []

    return tasks


def get_task_details(project, task_name):
    for details in get_fabric_tasks(project):
        if details[0] == task_name:
            return details

    return None


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
            del session['configuration_values'][key]

    arg_values = session.get('configuration_values', {})

    return configs, arg_values


def build_command(deployment, session, abort_on_prompts=True):
    # Get the dictionary of configurations for this stage
    configs = deployment.stage.get_configurations()
    configs, arg_values = update_config_values_from_session(configs, session)

    task_args = [key for key, config in configs.iteritems() if config.task_argument and config.task_name == deployment.task.name]
    task_configs = [key for key, config in configs.iteritems() if not config.task_argument]

    command_to_config = {x.replace('-', '_'): x for x in fabric_special_options}

    # Take the special env variables out
    normal_task_configs = list(set(task_configs) - set(command_to_config.keys()))

    # Special ones get set a different way
    special_task_configs = list(set(task_configs) & set(command_to_config.keys()))

    command = 'fab ' + deployment.task.name

    task_details = get_task_details(deployment.stage.project, deployment.task.name)

    task_args = list(set(task_args + [x[0] if isinstance(x, tuple) else x for x in task_details[2]]))

    if task_args:
        key_value_strings = []
        for key in task_args:
            if key in configs:
                value = unicode(configs[key].get_value())
            elif key in arg_values:
                value = unicode(arg_values[key])
            else:
                continue

            cleaned_key = clean_arg_key_string(key)
            value = clean_value_string(value)
            key_value_strings.append('{}="{}"'.format(cleaned_key, value))

        if key_value_strings:
            command += ':'
            command += ','.join(key_value_strings)

    if normal_task_configs:
        command += ' --set '
        command += '"' + ','.join(get_key_value_string(key, configs[key]) for key in normal_task_configs) + '"'

    if special_task_configs:
        for key in special_task_configs:
            if key == 'key_filename':
                command += ' -i ' + configs[key].get_value()
            else:
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
