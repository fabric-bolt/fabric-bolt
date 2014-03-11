Fabric Bolt
===========

A web interface for fabric deployments.

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

Examples Screens
----------------

.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.34.45%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.35.16%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.35.44%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.35.55%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.36.06%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.36.28%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.37.19%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.37.29%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.37.35%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.37.42%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.37.48%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.37.54%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.38.03%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.38.25%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.40.08%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.40.24%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.40.34%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.41.53%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.42.18%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.42.30%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.42.37%20PM.png
.. image:: https://raw.github.com/worthwhile/fabric-bolt/master/docs/images/Screen%20Shot%202013-09-29%20at%207.43.28%20PM.png

Authors
-------

* Dan Dietz
* Jared Proffitt
* Nathaniel Pardington
