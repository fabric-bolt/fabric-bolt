Overview
========

Hosts
-----

Hosts are simply an IP address or DNS name. Hosts are globally defined and can be targets for several projects in Fabric Bolt. 

Host Roles
----------

It is common to have hosts that perform a particular role. For instance we might have a host that is a database server, one that is a web server, and one that is an app server (performing background tasks). By specifying what role each host plays, Fabric Bolt can customize the commands that run against each host during a deployment. So database servers have migrations run against them and web servers have their static assets collected to a central place, but not vice versa.

Sometimes a particular host serves as a particular role for one project, but a different role for another project. So roles are assigned to hosts when you configure them on a project.

Projects
--------

Projects are simply a deployment configuration. Each project can define a top level Project Configuration that includes things like the source control location, source code branch to use, host connection credentials, etc. 

Projects also define their stages (more on stages below).

Project Stages
--------------

It is common for web developers to deploy their projects to a test/development/staging host for review before deploying to production. In Fabric Bolt we refer to those pieces of a deployment workflow as stages. In other words, we would always go through the following deployment stages for a particular project revision:

test -> staging -> production

Because stages can be as unique as the project code base itself, stages are configured per project and define stage specific configuration values that can override project configurations. Each Stage is simply a Host, Host Role, and Configuration values.

Deployment Tasks
----------------

Fabric Bolt uses a python package called Fabric to provide the core functionality of connecting to a remote host and executing shell commands on that host to perform a deployment. Because deployments typically have a large collection of commands that must be executed on a remote host, and those commands are usually grouped together to perform a particular deployment task, Fabric Bolt leverages Fabric tasks as deployment tasks. A deployment task is the same thing as a Fabric task, which is a collection of remote commands to run.

Deployment tasks are defined in a fabfile.py file that ships with Fabric Bolt. But you can provide your own fabfile.py if you want to customize the deployment tasks for a project.

Your deployment tasks are defined at the project level, but because Project Stages are the full configuration of a project and target host, deployment tasks are run from the project stage page.


Putting it Together
-------------------

If we diagram this simple structure, it looks something like this::

	Project
	|_ Configurations (git repo, git branch, code_root, etc.)
	|_ Deployment Tasks
	|
	|_ Test Stage
	|  |_ Hosts (w/ roles)
	|  |_ Configurations (git branch, settings_file, etc.)
	|
	|_ Production Stage
	  |_ Hosts (w/ roles)
	  |_ Configurations (git branch, settings_file, etc.)
	  

Running a Deployment
---------------------

Deployments are actually run against a project stage, since project stages fully define both the project and target hosts fully. To run a deployment:

1. Define your hosts
2. Create a project
3. Configure the project with the source control repo to be deployed (and any other necessary configs)
4. Add a stage
5. Configure the stage with at least one host
6. Select a deployment task to run against the stage
7. Review the deployment details and provide comments about the deployment
8. Click "Go!"

Deployments run in a background thread so you can navigate away from the deployment detail screen while a deployment is running. Fabric Bolt tracks the status of the deployment so that you can always come back later and check for success. However, from the deployment detail screen you can watch the live log of what commands are being run on the remote hosts while a deployment is running. After the deployment is complete the log is available for review. This is particularly helpful for resolving issues with failed deployments.

Users
-----

Users are configured in the system with one of three roles. For details on these roles see the http://yourdomain.com/user/permissions/ page.