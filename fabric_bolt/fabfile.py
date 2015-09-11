import cgi
import datetime
import time
from tempfile import NamedTemporaryFile

from fabric.api import *
from fabric import colors


@task
def update():
    """Requires code_root env variable. Does a git pull and restarts the web server"""
    require('code_root')

    git_pull()

    restart_web_server()


@task
def git_pull():
    """Does a git stash then a git pull on the project"""
    run('cd %s; git stash; git pull' % (env.code_root))


@task
def restart_web_server():
    """Restart the web server"""
    run('%s/apache2/bin/restart' % env.code_root_parent)


@task
def migrate():
    """Runs python manage.py migrate"""
    run('cd %s; python manage.py migrate --settings=%s' % (env.code_root, env.settings_file))


@task
def collect_static():
    """Runs python manage.py collect_static --noinput"""
    run('cd %s; python manage.py collectstatic --settings=%s --noinput' % (env.code_root, env.settings_file))


@task
def pip_install():
    """Runs pip install -r requirements/frozen.txt (for example site)"""
    run('cd %s; pip install -r requirements/frozen.txt' % (env.code_root))


@task
def publish_changes():
    """Runs these functions in order (git_pull, pip_install, migrate, collect_static, restart_web_server)"""
    git_pull()
    pip_install()
    migrate()
    collect_static()
    restart_web_server()


@task
def do_nothing():
    for x in range(0, 20):
        print 'nothing {}'.format(x)
        time.sleep(0.2)

    input = prompt('Enter something:')

    for x in range(0, 20):
        print 'nothing {} - {}'.format(x, input)
        time.sleep(0.2)


@task
def color_test():
    for x in range(0, 2):
        print colors.blue('Blue text', bold=False) + '\n'
        time.sleep(0.2)
        print colors.cyan('cyan text', bold=False)
        time.sleep(0.2)
        print colors.green('green text', bold=False)
        time.sleep(0.2)
        print colors.magenta('magenta text', bold=False)
        time.sleep(0.2)
        print colors.red('red text', bold=False)
        time.sleep(0.2)
        print colors.white('white text', bold=False)
        time.sleep(0.2)
        print colors.yellow('yellow text', bold=False)
        time.sleep(0.2)
        print colors.blue('Blue text bold', bold=True)
        time.sleep(0.2)
        print colors.cyan('cyan text bold', bold=True)
        time.sleep(0.2)
        print colors.green('green text bold', bold=True)
        time.sleep(0.2)
        print colors.magenta('magenta text bold', bold=True)
        time.sleep(0.2)
        print colors.red('red text bold', bold=True)
        time.sleep(0.2)
        print colors.white('white text bold', bold=True)
        time.sleep(0.2)
        print colors.yellow('yellow text bold', bold=True)
        time.sleep(0.2)

@task
def test_env(argument="nothing"):
    print("Task Arguments:")
    print argument
    print

    print("Task Env:")
    for x, y in env.iteritems():
        print '{}: {}'.format(x, y)


@task
def update_sandbox_site(comment_text):
    """put's a text file on the server"""

    file_to_deliver = NamedTemporaryFile(delete=False)

    file_text = "Deployed at: {} <br /> Comment: {}".format(datetime.datetime.now().strftime('%c'), cgi.escape(comment_text))

    file_to_deliver.write(file_text)
    file_to_deliver.close()

    put(file_to_deliver.name, '/var/www/html/index.html', use_sudo=True)
