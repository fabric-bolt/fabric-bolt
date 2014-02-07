.. Fabric Bolt documentation master file, created by
   sphinx-quickstart on Thu Nov 14 16:43:47 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Fabric Bolt's documentation!
=======================================

Build Status
------------

.. image:: https://travis-ci.org/worthwhile/fabric-bolt.png?branch=develop   
        :target: https://travis-ci.org/worthwhile/fabric-bolt

Quickstart
----------

1. Install::

    pip install fabric-bolt

2. Initialize settings file. (To specify file location, enter as the second argument.)::

    fabric-bolt init [~/.fabric-bolt/settings.py]

3. Modify generated settings file to enter database settings.

4. Migrate db::

    fabric-bolt syncdb --migrate

5. Run::

    fabric-bolt runserver

Note:

If you have created a settings file at a different location than the default, you can use the --config option on any
command (besides the init command) to specify the custom file path. Alternatively, you can set an env variable: FABRIC_BOLT_CONF.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

