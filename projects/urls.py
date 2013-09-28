from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import views

urlpatterns = patterns('',
    url(r'^$', views.ProjectList.as_view(), name='projects_project_list'),
    url(r'^create/$', views.ProjectCreate.as_view(), name='projects_project_create'),
    url(r'^update/(?P<pk>\w+)/$', views.ProjectUpdate.as_view(), name='projects_project_update'),
    url(r'^view/(?P<pk>\w+)/$', views.ProjectView.as_view(), name='projects_project_vie'),

)