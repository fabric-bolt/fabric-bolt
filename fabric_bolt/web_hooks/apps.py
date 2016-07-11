from django.apps import AppConfig


class WebHooksConfig(AppConfig):
    name = 'web_hooks'
    verbose_name = "Web Hooks"

    def ready(self):
        # register the signals
        from . import receivers