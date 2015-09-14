from django.conf.urls import url, include
from fabric_bolt import task_runners

from fabric_bolt.projects import views


urlpatterns = [
    url(r'^$', views.ProjectList.as_view(), name='projects_project_list'),

    url(r'^create/$', views.ProjectCreate.as_view(), name='projects_project_create'),

    url(r'^(?P<pk>\w+)/$', views.ProjectDetail.as_view(), name='projects_project_view'),
    url(r'^(?P<pk>\w+)/update/$', views.ProjectUpdate.as_view(), name='projects_project_update'),
    url(r'^(?P<pk>\w+)/delete/$', views.ProjectDelete.as_view(), name='projects_project_delete'),
    url(r'^(?P<pk>\w+)/invalidate-cache/$', views.ProjectInvalidateCache.as_view(), name='projects_project_invalidate_cache'),
    url(r'^(?P<pk>\w+)/copy/$', views.ProjectCopy.as_view(), name='projects_project_copy'),

    url(r'^(?P<project_id>\w+)/configuration/$', views.ProjectConfigurationList.as_view(), name='projects_configuration_list'),
    url(r'^(?P<project_id>\w+)/configuration/create/$', views.ProjectConfigurationCreate.as_view(), name='projects_configuration_create'),
    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\d+)/configuration/create/$', views.ProjectConfigurationCreate.as_view(), name='projects_configuration_stage_create'),
    url(r'^(?P<project_id>\w+)/configuration/(?P<pk>\w+)/update/$', views.ProjectConfigurationUpdate.as_view(), name='projects_configuration_update'),
    url(r'^(?P<project_id>\w+)/configuration/(?P<pk>\w+)/delete/$', views.ProjectConfigurationDelete.as_view(), name='projects_configuration_delete'),

    url(r'^(?P<project_id>\w+)/deployment/$', views.ProjectDeploymentList.as_view(), name='projects_deployment_list'),
    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\d+)/deployment/create/$', views.DeploymentCreate.as_view(), name='projects_deployment_create'),
    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\d+)/deployment/(?P<pk>\d+)/$', views.DeploymentDetail.as_view(), name='projects_deployment_detail'),
    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\d+)/deployment/(?P<pk>\d+)/', include(task_runners.backend.get_urls())),

    url(r'^(?P<project_id>\w+)/stage/$', views.ProjectStageList.as_view(), name='projects_stage_list'),
    url(r'^(?P<project_id>\w+)/stage/create/$', views.ProjectStageCreate.as_view(), name='projects_stage_create'),
    url(r'^(?P<project_id>\w+)/stage/(?P<pk>\w+)/$', views.ProjectStageView.as_view(), name='projects_stage_view'),
    url(r'^(?P<project_id>\w+)/stage/(?P<pk>\w+)/update/$', views.ProjectStageUpdate.as_view(), name='projects_stage_update'),
    url(r'^(?P<project_id>\w+)/stage/(?P<pk>\w+)/get-tasks-ajax/$', views.ProjectStageTasksAjax.as_view(), name='projects_stage_tasks_ajax'),
    url(r'^(?P<project_id>\w+)/stage/(?P<pk>\w+)/delete/$', views.ProjectStageDelete.as_view(), name='projects_stage_delete'),

    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\w+)/configuration/$', views.StageConfigurationList.as_view(), name='projects_stage_configuration_list'),
    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\w+)/deployment/$', views.StageDeploymentList.as_view(), name='projects_stage_deployment_list'),
    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\w+)/host/(?P<host_id>\w+)/map/$', views.ProjectStageMapHost.as_view(), name='projects_stage_maphost'),
    url(r'^(?P<project_id>\w+)/stage/(?P<stage_id>\w+)/host/(?P<host_id>\w+)/unmap/$', views.ProjectStageUnmapHost.as_view(), name='projects_stage_unmaphost'),
]
