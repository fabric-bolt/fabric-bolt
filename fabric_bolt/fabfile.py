import cgi
import datetime
import time
from tempfile import NamedTemporaryFile

from fabric.api import *


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

    # env.user = 'root'
    # env.key = '''-----BEGIN RSA PRIVATE KEY-----
    # MIIEowIBAAKCAQEArBsTE4MxG/x5PVcL4bNgvcIVJPdS2xWzmZkMZMeOkKx5y+Ew
    # DWT0nxU6iZn59M4p5B+xcxCzilnu0ljzeooxUbFRR/2jdvuAVEQRXcAFi17WtHP3
    # Up7U/t+vBmv2ZNLAlOn6U10rw36+wPmiG/yKTp9kYNfCE9B0+RS/5DPHbR2FS84D
    # 49vxruJKMH9zW0A0Me+PskOQtKCcDxT966Z2MsNZiPBti5ZK4yrjDYBM8E9PfXzJ
    # tlL/j6G8Z8ALm/MA4VypVMUEaRuRu8TfoMoTAeB2ixRYjoTJMi6r8s7WLOXaGmuV
    # g3Z1Gj20sdo2Fi5ordBSm+DDxVHxIBE4iRWkAQIDAQABAoIBAB1u4+xKW3O10eYz
    # pMyMqNbLAmK4CWt+YqC6E+yIVFFZrdq4QEeKJGuwbbpqotzDBVcGNIrBKHNYvgcr
    # PziNubGG6aeuMO6ARIokufOWi1wyc/WYf4uZrkOIbZ5jiFfl0xmkijMHlBxy6JyI
    # FLlEj0Ky76/ANmi9FcQjUE3urQRz6CaDHTjNGAK9qlh61GknGSb99E7BhGMigYkY
    # tVDw3RdQtaVJD0XcTpT/e6H3u6IelL3GS+F+JYpgHUC2gEMRTX8qluuLk8zjzNV8
    # qS0CXmOXNcCKbJjxWVxXubAlclHfLnpAU9s+Dvp3X+qs1N2LdGyNE+LpGvQe9MDp
    # Mg0pKaECgYEA2jbW7QGA7mpsUqdzdXLbVTihq5EqjPSLSVbI1h/z+DGVtsgCDwEd
    # +7EeB4tU/RNb5Ky+DGWjGEm2Rw+ntjhwO58lMh45eE2Z4vGnfkKo9uOMlWi/yH+b
    # tcB8t78cmazZXYK3dZgsjWsXf4FyQ6aJHIvwhN2xQRmGu2hX36S1IRMCgYEAyehO
    # KinudGEE7PrEbxt6MoYGL9pupELCE2oKC292PMRharPN7C2+7E+DbsDEfd4t6nEc
    # EzOWWADnFNh3VEGrsDwAgjgh8j2vgf35mLIaRXYXXcJlEtBIOVI9yOYOo8GdA/XV
    # yiOGVjjHrwVbWXCNULNKUsSmVN67HCOUXmlUHRsCgYBGF5Vj3bbHXkHbLtRkZndT
    # YXR0wpVTX32aGhk6xlq8X1kCtC4NGcPCw/qsW7H59Izw4BfPrZn8xDibjMjHPEu4
    # qv7soU6+eNa0UgEGCm1xmFfg6huoUGz4rZKiBu4t4pqTcdhyGmY9KqgKmc7VMhoa
    # pEymsPstuQBRFEwdly9jJwKBgEcvci+HbRz2/8eVeiA6LdEWU6QXfR7IsqgpoLT7
    # bVJrYnU+Q4Hbdw7V0d8Ac8Z0yPd5PY6/h2grmU1OLHQ2WxPdc8h1hfJkMTbBlnhx
    # grWutvpFiWEisfQTvNjR06OEpZk52VBVSg2oIy7f0p8sAYbMT43y6znM9WcsXCkV
    # NaS1AoGBAM8jX1zQP/jo1PWuwjzX38xyoDeludCmT09YRsC4C41LbI1Wj8mfxrf5
    # bQiPkbIZOeTG6ivvPbKbiwF5W+i92W+uUag5kotG+xCQUrWDrj2ELxRbAetT4dRh
    # vv+QoeHlCNRQ+2lsHIoqcAPFCXw6HTT5O/0MIAcEZICT7nf6znXX
    # -----END RSA PRIVATE KEY-----'''

    file_to_deliver = NamedTemporaryFile(delete=False)

    file_text = "Deployed at: {} <br /> Comment: {}".format(datetime.datetime.now().strftime('%c'), cgi.escape(comment_text))

    file_to_deliver.write(file_text)
    file_to_deliver.close()

    put(file_to_deliver.name, '/var/www/html/index.html', use_sudo=True)
