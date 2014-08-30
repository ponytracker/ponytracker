from django.conf.urls import url, include


urlpatterns = [
    # Global permissions
    url(r'^admin/permissions/$', 'permissions.views.global_perm_list', name='list-global-permission'),
    url(r'^admin/permissions/add/$', 'permissions.views.global_perm_edit', name='add-global-permission'),
    url(r'^admin/permissions/(?P<id>[0-9]+)/edit/$', 'permissions.views.global_perm_edit', name='edit-global-permission'),
    url(r'^admin/permissions/(?P<id>[0-9]+)/delete/$', 'permissions.views.global_perm_delete', name='delete-global-permission'),
    url(r'^admin/permissions/(?P<id>[0-9]+)/toggle/(?P<perm>[a-z-]+)/$', 'permissions.views.global_perm_toggle', name='toggle-global-permission'),
    # Project permissions
    url(r'^(?P<project>[-\w]+)/permissions/$', 'permissions.views.project_perm_list', name='list-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/add/$', 'permissions.views.project_perm_edit', name='add-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/(?P<id>[0-9]+)/edit/$', 'permissions.views.project_perm_edit', name='edit-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/(?P<id>[0-9]+)/delete/$', 'permissions.views.project_perm_delete', name='delete-project-permission'),
    url(r'^(?P<project>[-\w]+)/permissions/(?P<id>[0-9]+)/toggle/(?P<perm>[a-z-]+)/$', 'permissions.views.project_perm_toggle', name='toggle-project-permission'),
]
