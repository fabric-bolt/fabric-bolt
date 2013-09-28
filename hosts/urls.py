from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import views

urlpatterns = patterns('',
    url(r'^$', views.HostList.as_view(), name='hosts_host_list'),
    url(r'^create$', views.HostCreate.as_view(), name='hosts_host_create'),
)