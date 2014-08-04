FAQ
===

What is the difference between a role and a host?

Fabric Bolt hosts are globally known servers that Fabric Bolt can deploy to. When configuring a stage you need to add servers to it in order to deploy it. Each time you add a host you give it a role like app. This host is then used by the stage as a application-server. You can also create your own custom roles like ferret_server and reference this role in a task.

How do I run a deployment?

Fabric Bolt uses the concept of Project Stages to allow for sufficient customization for a deployment. You will need to configure at least one host, one project, and one project stage. Once those items are properly configured you can select a deployment task to run on the Project Stage page.

