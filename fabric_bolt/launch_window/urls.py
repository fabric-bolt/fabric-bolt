from django.conf.urls import patterns, url

from fabric_bolt.launch_window import views


urlpatterns = patterns('',
    url(r'^list/$', views.LaunchWindowList.as_view(), name='launch_window_launchwindow_list'),
    url(r'^(?P<pk>\d+)/', views.LaunchWindowDetail.as_view(), name='launch_window_launchwindow_detail'),
    url(r'^create/$', views.LaunchWindowCreate.as_view(), name='launch_window_launchwindow_create'),
    url(r'^update/(?P<pk>\d+)/', views.LaunchWindowUpdate.as_view(), name='launch_window_launchwindow_update'),
    url(r'^delete/(?P<pk>\d+)/', views.LaunchWindowDelete.as_view(), name='launch_window_launchwindow_delete'),
)