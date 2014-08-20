from django.dispatch import receiver

from fabric_bolt.web_hooks.utils import deliver_hook, payload_generator
from fabric_bolt.projects.signals import deployment_finished
from fabric_bolt.projects.models import Deployment


@receiver(deployment_finished)
def web_hook_receiver(sender, **kwargs):
    """Generic receiver for the web hook firing piece."""

    deployment = Deployment.objects.get(pk=kwargs.get('deployment_id'))

    hooks = deployment.web_hooks

    if not hooks:
        return

    for hook in hooks:

        data = payload_generator(deployment)

        deliver_hook(deployment, hook.url, data)
