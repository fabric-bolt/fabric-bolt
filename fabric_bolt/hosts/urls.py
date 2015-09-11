from django.conf.urls import url

from fabric_bolt.hosts import views


urlpatterns = [
    url(r'^$', views.HostList.as_view(), name='hosts_host_list'),
    url(r'^create/$', views.HostCreate.as_view(), name='hosts_host_create'),
    url(r'^(?P<pk>\d+)/$', views.HostDetail.as_view(), name='hosts_host_detail'),
    url(r'^(?P<pk>\d+)/update/$', views.HostUpdate.as_view(), name='hosts_host_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.HostDelete.as_view(), name='hosts_host_delete'),

    url(r'sshconfig/$', views.SSHKeys.as_view(), name='hosts_ssh_config'),
    url(r'sshconfig/create/$', views.SSHKeysCreate.as_view(), name='hosts_ssh_config_create'),

    url(r'sshconfig/(?P<pk>\d+)/delete/$', views.SSHKeyDelete.as_view(), name='hosts_ssh_config_delete'),

]
