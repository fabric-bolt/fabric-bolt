# Copyright (c) 2012 Zapier LLC.
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is
# hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
# AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import requests
import json

from django.conf import settings
from django.core import serializers
from django.core.urlresolvers import reverse

if getattr(settings, 'HOOK_THREADING', True):
    from .client import Client
    client = Client()
else:
    client = requests


def get_module(path):
    """
    A modified duplicate from Django's built in backend
    retriever.

        slugify = get_module('django.template.defaultfilters.slugify')
    """
    from importlib import import_module

    try:
        mod_name, func_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError, e:
        raise ImportError(
            'Error importing alert function {0}: "{1}"'.format(mod_name, e))

    try:
        func = getattr(mod, func_name)
    except AttributeError:
        raise ImportError(
            ('Module "{0}" does not define a "{1}" function'
                            ).format(mod_name, func_name))

    return func


def serialize_hook(instance):
    """
    Serialize the object down to Python primitives.

    By default it uses Django's built in serializer.
    """

    if getattr(instance, 'serialize_hook', None) and callable(instance.serialize_hook):
        return instance.serialize_hook(hook=instance)
    if getattr(settings, 'HOOK_SERIALIZER', None):
        serializer = get_module(settings.HOOK_SERIALIZER)
        return serializer(instance, hook=instance)
    # if no user defined serializers, fallback to the django builtin!
    return {
        'hook': instance.dict(),
        'data': serializers.serialize('python', [instance])[0]
    }


def deliver_hook(instance, target, payload_override=None):
    """
    Deliver the payload to the target URL.

    By default it serializes to JSON and POSTs.
    """
    payload = payload_override or serialize_hook(instance)
    if hasattr(settings, 'HOOK_DELIVERER'):
        deliverer = get_module(settings.HOOK_DELIVERER)
        deliverer(target, payload, instance=instance)
    else:
        client.post(
            url=target,
            data=json.dumps(payload, cls=serializers.json.DjangoJSONEncoder),
            headers={'Content-Type': 'application/json'}
        )

    return None


def get_payload(deployment):

    return {
        "event_name": "deployment_create",
        "id": deployment.pk,
        "url": reverse('projects_deployment_detail', args=(deployment.stage.project_id, deployment.stage_id, deployment.pk,)),
        "status": deployment.status,
        "task": {
            "name": deployment.task.name
        },
        "date_deleted": '',
        "date_update": '',
        "comments": deployment.comments,
        "user": {
            "id": deployment.user.pk,
            "name": '{} {}'.format(deployment.user.first_name, deployment.user.last_name),
            "email": deployment.user.email
        },
        "output": deployment.output,
        "date_created": '',
        "configuration": '',
        "stage": {
            "id": deployment.stage.pk,
            "name": deployment.stage.name,
            "url": reverse('projects_stage_view', args=(deployment.stage.project.pk, deployment.stage.pk))
        }
    }


if hasattr(settings, 'DEPLOYMENT_FINISHED_PAYLOAD_GENERATOR'):
    payload_generator = settings.DEPLOYMENT_FINISHED_PAYLOAD_GENERATOR
else:
    payload_generator = get_payload