from django.conf.urls import url, patterns, include

from fabric_bolt.accounts import views

urlpatterns = patterns('',

    url(r'^user/permissions/$', views.UserPermissions.as_view(), name='accounts_user_permissions'),

    url(r'^users/$', views.UserList.as_view(), name='accounts_user_list'),
    url(r'^user/add/$', views.UserAdd.as_view(), name='accounts_user_add'),
    url(r'^user/change/(?P<pk>.+)/$', views.UserChange.as_view(), name='accounts_user_change'),
    url(r'^user/delete/(?P<pk>.+)/$', views.UserDelete.as_view(), name='accounts_user_delete'),
    url(r'^user/(?P<pk>.+)/$', views.UserDetail.as_view(), name='accounts_user_view'),

    url(r'^password_change/$', views.PasswordChange.as_view(), name='password_change'),
    url(r'^logout/$', 'authtools.views.logout_then_login', name='logout'),

    url(r'^', include('authtools.urls'))
)