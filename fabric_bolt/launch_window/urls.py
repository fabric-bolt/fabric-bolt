from django.conf.urls import  url

from fabric_bolt.launch_window import views


urlpatterns = [
    url(r'^$', views.LaunchWindowList.as_view(), name='launch_window_launchwindow_list'),
    url(r'^(?P<pk>\d+)/$', views.LaunchWindowDetail.as_view(), name='launch_window_launchwindow_detail'),
    url(r'^(?P<pk>\d+)/update/$', views.LaunchWindowUpdate.as_view(), name='launch_window_launchwindow_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.LaunchWindowDelete.as_view(), name='launch_window_launchwindow_delete'),
    url(r'^create/$', views.LaunchWindowCreate.as_view(), name='launch_window_launchwindow_create'),
]
