from fabric.api import *


def update():
    require('code_root')

    git_pull()

    restart_web_server()


def git_pull():
    run('cd %s; git stash; git pull' % (env.code_root))


def restart_web_server():
    "Restart the web server"
    run('%s/apache2/bin/restart' % env.code_root_parent)


def migrate():
    run('cd %s; python manage.py migrate --settings=%s' % (env.code_root, env.settings_file))


def collect_static():
    run('cd %s; python manage.py collectstatic --settings=%s --noinput' % (env.code_root, env.settings_file))


def pip_install():
    run('cd %s; pip install -r requirements/frozen.txt' % (env.code_root))


def publish_changes():
    update()
    pip_install()
    migrate()
    collect_static()
    restart_web_server()