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

from celery.task import Task

from django.core.serializers.json import DjangoJSONEncoder

from fabric_bolt.web_hooks.models import Hook


class DeliverHook(Task):
    def run(self, target, payload, instance=None, hook_id=None, **kwargs):
        """
        target:     the url to receive the payload.
        payload:    a python primitive data structure
        instance:   a possibly null "trigger" instance
        hook:       the defining Hook object (useful for removing)
        """
        self.post_data(target, payload, hook_id)

    def post_data(self, target, payload, hook_id=None):

        response = requests.post(
            url=target,
            data=json.dumps(payload, cls=DjangoJSONEncoder),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 410 and hook_id:
            hook = Hook.objects.get(pk=hook_id)
            hook.delete()

        return response


def deliver_hook_wrapper(target, payload, instance=None, hook=None, **kwargs):
    if hook:
        kwargs['hook_id'] = hook.id
    return DeliverHook().delay(target, payload, **kwargs)
