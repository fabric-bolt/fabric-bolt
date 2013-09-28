from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import views

urlpatterns = patterns('',
    url(r'^projects/$', views.CreateProject.as_view(), name='projects_project_create'),
    url(r'^project/create/$', views.CreateProject.as_view(), name='projects_project_create'),
    url(r'^edit/project/(?P<pk>\w+)/$', views.EditProject.as_view(), name='projects_project_edit'),
)