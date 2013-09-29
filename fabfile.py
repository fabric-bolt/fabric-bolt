from fabric.api import *


def update():
    """Requires code_root env variable. Does a git pull and restarts the web server"""
    require('code_root')

    git_pull()

    restart_web_server()


def git_pull():
    """Does a git stash then a git pull on the project"""
    run('cd %s; git stash; git pull' % (env.code_root))


def restart_web_server():
    """Restart the web server"""
    run('%s/apache2/bin/restart' % env.code_root_parent)


def migrate():
    """Runs python manage.py migrate"""
    run('cd %s; python manage.py migrate --settings=%s' % (env.code_root, env.settings_file))


def collect_static():
    """Runs python manage.py collect_static --noinput"""
    run('cd %s; python manage.py collectstatic --settings=%s --noinput' % (env.code_root, env.settings_file))


def pip_install():
    """Runs pip install -r requirements/frozen.txt (for example site)"""
    run('cd %s; pip install -r requirements/frozen.txt' % (env.code_root))


def publish_changes():
    """Runs these functions in order (git_pull, pip_install, migrate, collect_static, restart_web_server)"""
    git_pull()
    pip_install()
    migrate()
    collect_static()
    restart_web_server()