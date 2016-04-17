from django.conf.urls import url, include

from accounts import views


urlpatterns = [
    # Profile
    url(r'^profile/$', views.profile, name='profile'),
    # Users
    url(r'^admin/users/$', views.user_list, name='list-user'),
    url(r'^admin/users/add/$', views.user_edit, name='add-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/$', views.user_details, name='show-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/edit/$', views.user_edit, name='edit-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/edit-password/$', views.user_edit_password, name='edit-user-password'),
    url(r'^admin/users/(?P<user>[0-9]+)/delete/$', views.user_delete, name='delete-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/activate/$', views.user_activate, name='activate-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/disable/$', views.user_disable, name='disable-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/add-group/$', views.user_add_group, name='add-group-to-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/remove-group/(?P<group>[0-9]+)/$', views.user_remove_group, name='remove-group-from-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/add-team/$', views.user_add_team, name='add-team-to-user'),
    url(r'^admin/users/(?P<user>[0-9]+)/remove-team/(?P<team>[0-9]+)/$', views.user_remove_team, name='remove-team-from-user'),
    # Groups
    url(r'^admin/groups/$', views.group_list, name='list-group'),
    url(r'^admin/groups/add/$', views.group_edit, name='add-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/$', views.group_details, name='show-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/edit/$', views.group_edit, name='edit-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/delete/$', views.group_delete, name='delete-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/add-user/$', views.group_add_user, name='add-user-to-group'),
    url(r'^admin/groups/(?P<group>[0-9]+)/remove-user/(?P<user>[0-9]+)/$', views.group_remove_user, name='remove-user-from-group'),
    # Teams
    url(r'^admin/teams/$', views.team_list, name='list-team'),
    url(r'^admin/teams/add/$', views.team_edit, name='add-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/$', views.team_details, name='show-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/edit$', views.team_edit, name='edit-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/delete$', views.team_delete, name='delete-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/add-user/$', views.team_add_user, name='add-user-to-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/remove-user/(?P<user>[0-9]+)/$', views.team_remove_user, name='remove-user-from-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/add-group/$', views.team_add_group, name='add-group-to-team'),
    url(r'^admin/teams/(?P<team>[0-9]+)/remove-group/(?P<group>[0-9]+)/$', views.team_remove_group, name='remove-group-from-team'),
]
