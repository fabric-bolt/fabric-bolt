from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy

from authtools.views import LogoutView

from fabric_bolt.accounts import views

urlpatterns = [

    url(r'^$', views.UserList.as_view(), name='accounts_user_list'),
    url(r'^(?P<pk>\d+)/$', views.UserDetail.as_view(), name='accounts_user_view'),
    url(r'^(?P<pk>\d+)/update/$', views.UserChange.as_view(), name='accounts_user_change'),
    url(r'^(?P<pk>\d+)/delete/$', views.UserDelete.as_view(), name='accounts_user_delete'),

    url(r'^add/$', views.UserAdd.as_view(), name='accounts_user_add'),
    url(r'^permissions/$', views.UserPermissions.as_view(), name='accounts_user_permissions'),

    url(r'^password_change/$', views.PasswordChange.as_view(), name='password_change'),
    url(r'^logout/$', LogoutView.as_view(url=reverse_lazy('login')), name='logout'),

    url(r'^', include('authtools.urls'))
]
