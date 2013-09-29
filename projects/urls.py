from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import views

urlpatterns = patterns('',
    url(r'^$', views.ProjectList.as_view(), name='projects_project_list'),

    url(r'^create/$', views.ProjectCreate.as_view(), name='projects_project_create'),
    url(r'^view/(?P<pk>\w+)/$', views.ProjectDetail.as_view(), name='projects_project_view'),
    url(r'^update/(?P<pk>\w+)/$', views.ProjectUpdate.as_view(), name='projects_project_update'),
    url(r'^delete/(?P<pk>\w+)/$', views.ProjectDelete.as_view(), name='projects_project_delete'),

    url(r'^(?P<project_id>\w+)/configuration/create/$', views.ProjectConfigurationCreate.as_view(), name='projects_configuration_create'),
    url(r'^(?P<project_id>\w+)/configuration/stage/(?P<stage_id>\d+)/create/$', views.ProjectConfigurationCreate.as_view(), name='projects_configuration_stage_create'),
    url(r'^configuration/update/(?P<pk>\w+)/$', views.ProjectConfigurationUpdate.as_view(), name='projects_configuration_update'),
    url(r'^configuration/delete/(?P<pk>\w+)/$', views.ProjectConfigurationDelete.as_view(), name='projects_configuration_delete'),

    url(r'^stage/(?P<pk>\d+)/deployment/(?P<task_name>\w+)/$', views.DeploymentCreate.as_view(), name='projects_deployment_create'),
    url(r'^deployment/view/(?P<pk>\d+)', views.DeploymentDetail.as_view(), name='projects_deployment_detail'),
    url(r'^deployment/output/(?P<pk>\d+)', views.DeploymentOutputStream.as_view(), name='projects_deployment_output'),

    url(r'^(?P<project_id>\w+)/stage/create/$', views.ProjectStageCreate.as_view(), name='projects_stage_create'),
    url(r'^(?P<project_id>\w+)/stage/update/(?P<pk>\w+)/$', views.ProjectStageUpdate.as_view(), name='projects_stage_update'),
    url(r'^(?P<project_id>\w+)/stage/view/(?P<pk>\w+)/$', views.ProjectStageView.as_view(), name='projects_stage_view'),

)