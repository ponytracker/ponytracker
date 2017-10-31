from django.conf.urls import url, include

from tracker import views, api


urlpatterns = [
    url(r'^markdown/$', views.markdown_preview, name='markdown'),
    # API
    url(r'^api/email/recv/$', api.email_recv, name='recv-email'),
    # Administration: redirect on first available admin page
    url(r'^admin/$', views.admin, name='admin'),
    # Settings
    url(r'^admin/settings/$', views.settings_list, name='settings'),
    # Projects
    url(r'^$', views.project_list, name='list-project'),
    url(r'^archived/$', views.project_list, {'archived': True}, name='list-archived-project'),
    url(r'^add/$', views.project_add, name='add-project'),
    url(r'^(?P<project>[-\w]+)/edit/$', views.project_edit, name='edit-project'),
    url(r'^(?P<project>[-\w]+)/delete/$', views.project_delete, name='delete-project'),
    url(r'^(?P<project>[-\w]+)/subscribe/$', views.project_subscribe, name='subscribe-project'),
    url(r'^(?P<project>[-\w]+)/unsubscribe/$', views.project_unsubscribe, name='unsubscribe-project'),
    url(r'^(?P<project>[-\w]+)/markread/$', views.project_mark_as_read, name='mark-read'),
    url(r'^(?P<project>[-\w]+)/archive/$', views.project_archive, {'archive': True}, name='archive-project'),
    url(r'^(?P<project>[-\w]+)/unarchive/$', views.project_archive, {'archive': False}, name='unarchive-project'),
    # Issues
    url(r'^(?P<project>[-\w]+)/issues/$', views.issue_list, name='list-issue'),
    url(r'^(?P<project>[-\w]+)/issues/add/$', views.issue_edit, name='add-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/$', views.issue_details, name='show-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/edit/$', views.issue_edit, name='edit-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/delete/$', views.issue_delete, name='delete-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/close/$', views.issue_close, name='close-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/reopen/$', views.issue_reopen, name='reopen-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/comment/$', views.issue_comment_edit, name='add-comment'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/comments/(?P<comment>[0-9]+)/edit/$', views.issue_comment_edit, name='edit-comment'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/comments/(?P<comment>[0-9]+)/delete/$', views.issue_comment_delete, name='delete-comment'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/subscribe/$', views.issue_subscribe, name='subscribe-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/unsubscribe/$', views.issue_unsubscribe, name='unsubscribe-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/add-label/(?P<label>[0-9]+)/$', views.issue_add_label, name='add-label-to-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/remove-label/(?P<label>[0-9]+)/$', views.issue_remove_label, name='remove-label-from-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/add-milestone/(?P<milestone>[a-z0-9_.-]+)/$', views.issue_add_milestone, name='add-milestone-to-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/remove-milestone/(?P<milestone>[a-z0-9_.-]+)/$', views.issue_remove_milestone, name='remove-milestone-from-issue'),
    # Labels
    url(r'^(?P<project>[-\w]+)/labels/$', views.label_list, name='list-label'),
    url(r'^(?P<project>[-\w]+)/labels/add/$', views.label_edit, name='add-label'),
    url(r'^(?P<project>[-\w]+)/labels/(?P<id>[0-9]+)/edit/$', views.label_edit, name='edit-label'),
    url(r'^(?P<project>[-\w]+)/labels/(?P<id>[0-9]+)/delete/$', views.label_delete, name='delete-label'),
    # Milestones
    url(r'^(?P<project>[-\w]+)/milestones/$', views.milestone_list, name='list-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/add/$', views.milestone_edit, name='add-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/edit/$', views.milestone_edit, name='edit-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/close/$', views.milestone_close, name='close-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/reopen/$', views.milestone_reopen, name='reopen-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/delete/$', views.milestone_delete, name='delete-milestone'),
    # Activities
    url(r'^(?P<project>[-\w]+)/activity/$', views.activity, name='show-activity'),
    # Default redirection
    url(r'^(?P<project>[-\w]+)/$', views.project_redirect),
]
