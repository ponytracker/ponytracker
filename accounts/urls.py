from django.conf.urls import url, include


urlpatterns = [
    # Profile
    url(r'^profile$', 'accounts.views.profile', name='profile'),
    # Users
    url(r'^admin/users/$', 'accounts.views.user_list', name='list-user'),
    url(r'^admin/users/add/$', 'accounts.views.user_edit', name='add-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/$', 'accounts.views.user_details', name='show-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/edit/$', 'accounts.views.user_edit', name='edit-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/delete/$', 'accounts.views.user_delete', name='delete-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/activate/$', 'accounts.views.user_activate', name='activate-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/disable/$', 'accounts.views.user_disable', name='disable-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/add-group/$', 'accounts.views.user_add_group', name='add-group-to-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/remove-group/(?P<group>[0-9]+)/$', 'accounts.views.user_remove_group', name='remove-group-from-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/add-team/$', 'accounts.views.user_add_team', name='add-team-to-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/remove-team/(?P<team>[0-9]+)/$', 'accounts.views.user_remove_team', name='remove-team-from-user'),
    # Groups
    url(r'^admin/groups/$', 'accounts.views.group_list', name='list-group'),
    url(r'^admin/groups/add/$', 'accounts.views.group_edit', name='add-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/$', 'accounts.views.group_details', name='show-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/edit/$', 'accounts.views.group_edit', name='edit-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/delete/$', 'accounts.views.group_delete', name='delete-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/add-user/$', 'accounts.views.group_add_user', name='add-user-to-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/remove-user/(?P<user>[0-9]+)/$', 'accounts.views.group_remove_user', name='remove-user-from-group'),
    # Teams
    url(r'^admin/teams/$', 'accounts.views.team_list', name='list-team'),
    url(r'^admin/teams/add/$', 'accounts.views.team_edit', name='add-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/$', 'accounts.views.team_details', name='show-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/edit$', 'accounts.views.team_edit', name='edit-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/delete$', 'accounts.views.team_delete', name='delete-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/add-user/$', 'accounts.views.team_add_user', name='add-user-to-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/remove-user/(?P<user>[0-9]+)/$', 'accounts.views.team_remove_user', name='remove-user-from-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/add-group/$', 'accounts.views.team_add_group', name='add-group-to-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/remove-group/(?P<group>[0-9]+)/$', 'accounts.views.team_remove_group', name='remove-group-from-team'),
]
