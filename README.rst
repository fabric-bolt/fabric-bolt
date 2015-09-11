FabricBolt
==========

.. image:: https://travis-ci.org/fabric-bolt/fabric-bolt.png?branch=master
        :target: https://travis-ci.org/fabric-bolt/fabric-bolt

.. image:: https://coveralls.io/repos/fabric-bolt/fabric-bolt/badge.svg?branch=master
        :target: https://coveralls.io/r/fabric-bolt/fabric-bolt?branch=master

| **tl;dr**
| A web interface for fabric deployments.


Fabric Bolt is a Python/Django project that allows you to deploy code stored in source control (a project) to a target server (host).
Fabric Bolt provides convenient web interfaces to configure both the projects and the hosts. Additionally, deployment history and
logs are stored so that you know who, what, where, when, and why something was deployed.

Documentation found at http://fabric-bolt.readthedocs.org/en/latest/

.. image:: http://fabricbolt.io/static/img/screen_deployments.png

Quickstart
----------

These steps are designed to get you rolling quickly, but more complete install/setup information is provided in our `documentation
<http://fabric-bolt.readthedocs.org/en/latest/>`_.

1. Install::

    pip install fabric-bolt

2. Initialize settings file. (To specify file location, enter as the second argument.)::

    fabric-bolt init [~/.fabric-bolt/settings.py]

3. Modify generated settings file to enter database settings.

4. Migrate db::

    fabric-bolt migrate

5. Create admin user, then follow the prompts to create an email and password::

    fabric-bolt [--config=~/.fabric-bolt/settings.py] createsuperuser

6. Run::

    fabric-bolt runserver

Note:

If you have created a settings file at a different location than the default, you can use the --config option on any
command (besides the init command) to specify the custom file path. Alternatively, you can set an env variable: FABRIC_BOLT_CONF.

Authors
-------

* Dan Dietz (paperreduction)
* Jared Proffitt (jproffitt)
* Nathaniel Pardington (npardington)


Bolting web applications to servers since 2013 :: Deploy Happy!
