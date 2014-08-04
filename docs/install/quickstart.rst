Fabric Bolt Quickstart
=======================

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