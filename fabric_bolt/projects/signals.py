import django.dispatch

deployment_finished = django.dispatch.Signal(providing_args=["deployment_id", ])
