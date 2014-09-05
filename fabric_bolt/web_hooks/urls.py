from django.conf.urls import patterns, url

from fabric_bolt.web_hooks import views


urlpatterns = patterns('',
    url(r'^create/$', views.HookCreate.as_view(), name='hooks_hook_create'),
    url(r'^create/(?P<project_id>\w+)/$', views.HookCreate.as_view(), name='hooks_hook_create_with_project'),
    url(r'^view/(?P<pk>\w+)/$', views.HookDetail.as_view(), name='hooks_hook_view'),
    url(r'^update/(?P<pk>\w+)/$', views.HookUpdate.as_view(), name='hooks_hook_update'),
    url(r'^delete/(?P<pk>\w+)/$', views.HookDelete.as_view(), name='hooks_hook_delete'),
)