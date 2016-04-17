from django.conf.urls import url, include

from permissions import views


urlpatterns = [
    # Global permissions
    url(r'^admin/permissions/$', views.global_perm_list, name='list-global-permission'),
    url(r'^admin/permissions/add/$', views.global_perm_edit, name='add-global-permission'),
    url(r'^admin/permissions/(?P<id>[0-9]+)/edit/$', views.global_perm_edit, name='edit-global-permission'),
    url(r'^admin/permissions/(?P<id>[0-9]+)/delete/$', views.global_perm_delete, name='delete-global-permission'),
    url(r'^admin/permissions/(?P<id>[0-9]+)/toggle/(?P<perm>[a-z_]+)/$', views.global_perm_toggle, name='toggle-global-permission'),
    # Project permissions
    url(r'^(?P<project>[-\w]+)/permissions/$', views.project_perm_list, name='list-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/add/$', views.project_perm_edit, name='add-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/(?P<id>[0-9]+)/edit/$', views.project_perm_edit, name='edit-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/(?P<id>[0-9]+)/delete/$', views.project_perm_delete, name='delete-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/(?P<id>[0-9]+)/toggle/(?P<perm>[a-z_]+)/$', views.project_perm_toggle, name='toggle-project-permission'),
]
