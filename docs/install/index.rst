Installing Fabric Bolt
======================

To run Fabric Bolt you'll need:

* A UNIX-based operating system
* Python 2.7
* python-setuptools, python-dev, libxslt1-dev, libxml2-dev
* A real database (PostgreSQL is preferred, MySQL also works)

You can run Fabric Bolt on an existing server/host, but this guide will assume that Fabric Bolt is
the only thing running on the server.

This guide will step you through setting up a virtualenv, installing the required packages,
and configuring the basic web service.

Quickstart
----------

If you are familiar with running a django project that has been pip installed, you can use these steps to
get Fabric Bolt running. Otherwise skip this and use the detailed directions below.

1. Install::

    pip install fabric-bolt

2. Initialize settings file. (To specify file location, enter as the second argument.)::

    fabric-bolt init [~/.fabric-bolt/settings.py]

3. Modify generated settings file to enter database settings.

4. Migrate db::

    fabric-bolt migrate

5. Run::

    fabric-bolt runserver

Note:

If you have created a settings file at a different location than the default, you can use the --config option on any
command (besides the init command) to specify the custom file path. Alternatively, you can set an env variable: FABRIC_BOLT_CONF.


Setting up an Environment
-------------------------

The first thing you'll need is the Python ``virtualenv`` package. You probably already
have this, but if not, you can install it with:

.. code-block:: bash

    easy_install -UZ virtualenv

Once that's done, choose a location for the environment, and create it with the ``virtualenv``
command. For our guide, we're going to choose ``/www/fabric-bolt/``:

.. code-block:: bash

    virtualenv /www/fabric-bolt/

Finally, activate your virtualenv:

.. code-block:: bash

  source /www/fabric-bolt/bin/activate

.. note:: Activating the environment adjusts your PATH, so that things like easy_install now
          install into the virtualenv by default.


Install Fabric Bolt
-------------------

Once you have the environment setup you can install Fabric Bolt and all its dependencies
with ``pip`` (``virtualenv`` comes with a copy of ``pip`` which gets copied into every
new environment you create):

.. code-block:: bash

    pip install fabric-bolt

Don't be worried by the amount of dependencies Fabric Bolt has. Our philosophy is to use the right tool for
the job, and to not reinvent them if they already exist.


Initializing the Configuration
------------------------------

After Fabric Bolt has been installed, you will need to create and configure a ``settings.py`` file.  We have packaged Fabric Bolt with a utility to generate a ``settings.py`` file for you:

.. code-block:: bash

    fabric-bolt init

Or, optionally, you can provide a path to the settings file:

.. code-block:: bash

    fabric-bolt init /etc/fabric-bolt/settings.py

The settings file will be located at ``~/.fabric-bolt/settings.py``. And should be edited for your database configuration:

.. code-block:: bash

    vi ~/.fabric-bolt/settings.py

The configuration for the server is based on the settings file, which contains a basic Django project configuration:

.. code-block:: python

    # ~/.fabric-bolt/settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # We suggest PostgreSQL for optimal performance
            'NAME': 'fabric-bolt',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {
                'autocommit': True,
            }
        }
    }


Configure Outbound Mail
-----------------------

Several settings exist as part of the Django framework which will configure your outbound mail server. For the
standard implementation, using a simple SMTP server, you can simply configure the following:

.. code-block:: python

    EMAIL_HOST = 'localhost'
    EMAIL_HOST_PASSWORD = ''
    EMAIL_HOST_USER = ''
    EMAIL_PORT = 25
    EMAIL_USE_TLS = False

Being that Django is a pluggable framework, you also have the ability to specify different mail backends. See the
`official Django documentation <https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#email-backends>`_ for
more information on alternative backends.


Running Migrations
------------------

Fabric Bolt provides an easy way to run migrations on the database on version upgrades. Before running it for
the first time you'll need to make sure you've created the database:

.. code-block:: bash

    # If you're using Postgres, and kept the database ``NAME`` as ``fabric-bolt``
    $ createdb -E utf-8 fabric-bolt

Once done, you can create the initial schema using the ``migrate`` command:

.. code-block:: bash

    $ fabric-bolt migrate

Next, create a super user by doing the following:

.. code-block:: bash

    # create a new user
    $ fabric-bolt --config=/etc/fabric-bolt/settings.py createsuperuser

All schema changes and database upgrades are handled via the ``migrate`` command, and this is the first
thing you'll want to run when upgrading to future versions of Fabric Bolt.

Starting the Web Service
------------------------

FOR TESTING, Fabric Bolt can be run with the basic webserver that comes packaged with django. This can be started
with ``fabric-bolt runserver``, or if you're using a custom settings file

::

  # Fabric Bolt's server runs on port 8000 by default. Make sure your client reflects
  # the correct host and port!
  fabric-bolt --config=/etc/fabric-bolt/settings.py runserver

You should now be able to test the web service by visiting `http://localhost:8000/`.

You should NOT run Fabric Bolt in production with ``runserver``. Follow the directions below to run Fabric Bolt with uWSGI and Nginx.

Setup a Reverse Proxy
---------------------

By default, Fabric Bolt runs on port 8000. Even if you change this, under normal conditions you won't be able to bind to
port 80. To get around this (and to avoid running Fabric Bolt as a privileged user, which you shouldn't), we recommend
you setup a simple web proxy.

Proxying with Apache
~~~~~~~~~~~~~~~~~~~~

Apache requires the use of mod_proxy for forwarding requests::

    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto "https" env=HTTPS

You will need to enable ``headers``, ``proxy``, and ``proxy_http`` apache modules to use these settings.

Proxying with Nginx
~~~~~~~~~~~~~~~~~~~

You'll use the builtin HttpProxyModule within Nginx to handle proxying::

    location / {
      proxy_pass         http://localhost:8000;
      proxy_redirect     off;

      proxy_set_header   Host              $host;
      proxy_set_header   X-Real-IP         $remote_addr;
      proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Proto $scheme;
    }

See :doc:`nginx` for more details on using Nginx.

Enabling SSL
~~~~~~~~~~~~~

If you are planning to use SSL, you will also need to ensure that you've
enabled detection within the reverse proxy (see the instructions above), as
well as within the Fabric Bolt configuration:

.. code-block:: python

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



Running Fabric Bolt as a Service
--------------------------------

We recommend using whatever software you are most familiar with for managing Fabric Bolt processes. For us, that software
of choice is `Supervisor <http://supervisord.org/>`_.

Configure ``supervisord``
~~~~~~~~~~~~~~~~~~~~~~~~~

Configuring Supervisor couldn't be more simple. Just point it to the ``fabric-bolt`` executable in your virtualenv's bin/
folder and you're good to go.

::

  [program:fabric-bolt-web]
  directory=/www/fabric-bolt/
  command=/www/fabric-bolt/bin/fabric-bolt start
  autostart=true
  autorestart=true
  redirect_stderr=true


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

