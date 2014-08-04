Configuring Fabric Bolt with Nginx
==================================

Nginx provides a very powerful platform for running in front of Fabric Bolt.

Below is a sample configuration for Nginx:

::

    http {

      server {
        listen   80;

        proxy_set_header   Host                 $http_host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
        proxy_redirect     off;

        # keepalive + raven.js is a disaster
        keepalive_timeout 0;

        # use very aggressive timeouts
        proxy_read_timeout 5s;
        proxy_send_timeout 5s;
        send_timeout 5s;
        resolver_timeout 5s;
        client_body_timeout 5s;

        # buffer larger messages
        client_max_body_size 150k;
        client_body_buffer_size 150k;

        location / {
          proxy_pass        http://localhost:8000;
        }

      }
    }


Proxying uWSGI
~~~~~~~~~~~~~~

We recommend that you setup `uWSGI <http://projects.unbit.it/uwsgi/>`_ to
run Fabric Bolt (rather than relying on the built-in django webserver).

Within your uWSGI configuration, you'll need to export your configuration path
as well the ``wsgi.py`` module:

::

    [uwsgi]
    env = FABRIC_BOLT_CONF=/etc/fabric-bolt/settings.py
    module = wsgi.py

    ; spawn the master and 4 processes
    http-socket = :8000
    master = true
    processes = 4

    ; allow longer headers for raven.js if applicable
    ; default: 4096
    buffer-size = 32768
