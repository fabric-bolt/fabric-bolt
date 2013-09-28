from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import views

urlpatterns = patterns('',
    url(r'^$', views.HostList.as_view(), name='hosts_host_list'),
    url(r'^create$', views.HostCreate.as_view(), name='hosts_host_create'),
    url(r'^update/(?P<pk>\d+)/', views.HostUpdate.as_view(), name='hosts_host_update'),
    url(r'^view/(?P<pk>\d+)/', views.HostDetail.as_view(), name='hosts_host_detail'),
    url(r'^delete/(?P<pk>\d+)/', views.HostDelete.as_view(), name='hosts_host_delete'),
)