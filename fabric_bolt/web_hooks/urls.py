from django.conf.urls import url

from fabric_bolt.web_hooks import views

urlpatterns = [
    url(r'^$', views.HookList.as_view(), name='hooks_hook_list'),
    url(r'^(?P<pk>\d+)/$', views.HookDetail.as_view(), name='hooks_hook_view'),
    url(r'^create/$', views.HookCreate.as_view(), name='hooks_hook_create'),
    url(r'^create/(?P<project_id>\d+)/$', views.HookCreate.as_view(), name='hooks_hook_create_with_project'),
    url(r'^(?P<pk>\d+)/update/$', views.HookUpdate.as_view(), name='hooks_hook_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.HookDelete.as_view(), name='hooks_hook_delete'),
]
