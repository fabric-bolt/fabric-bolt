from django.db import models


class Host(models.Model):
    '''Defines a Host'''

    name = models.CharField(max_length=255, help_text='DNS name or IP address')

    def __unicode__(self):
        return self.name