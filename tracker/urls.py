from django.conf.urls import url, include


urlpatterns = [
    url(r'^markdown/$', 'tracker.views.markdown_preview', name='markdown'),
    # API
    url(r'^api/email/recv/$', 'tracker.api.email_recv', name='recv-email'),
    # Administration: redirect on first available admin page
    url(r'^admin/$', 'tracker.views.admin', name='admin'),
    # Settings
    url(r'^admin/settings/$', 'tracker.views.settings_list', name='settings'),
    # Projects
    url(r'^$', 'tracker.views.project_list', name='list-project'),
    url(r'^add/$', 'tracker.views.project_add', name='add-project'),
    url(r'^(?P<project>[-\w]+)/edit/$', 'tracker.views.project_edit', name='edit-project'),
    url(r'^(?P<project>[-\w]+)/delete/$', 'tracker.views.project_delete', name='delete-project'),
    url(r'^(?P<project>[-\w]+)/subscribe/$', 'tracker.views.project_subscribe', name='subscribe-project'),
    url(r'^(?P<project>[-\w]+)/unsubscribe/$', 'tracker.views.project_unsubscribe', name='unsubscribe-project'),
    # Issues
    url(r'^(?P<project>[-\w]+)/issues/$', 'tracker.views.issue_list', name='list-issue'),
    url(r'^(?P<project>[-\w]+)/issues/add/$', 'tracker.views.issue_edit', name='add-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/$', 'tracker.views.issue_details', name='show-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/edit/$', 'tracker.views.issue_edit', name='edit-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/delete/$', 'tracker.views.issue_delete', name='delete-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/close/$', 'tracker.views.issue_close', name='close-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/reopen/$', 'tracker.views.issue_reopen', name='reopen-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/comment/$', 'tracker.views.issue_comment_edit', name='add-comment'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/comments/(?P<comment>[0-9]+)/edit/$', 'tracker.views.issue_comment_edit', name='edit-comment'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/comments/(?P<comment>[0-9]+)/delete/$', 'tracker.views.issue_comment_delete', name='delete-comment'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/subscribe/$', 'tracker.views.issue_subscribe', name='subscribe-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/unsubscribe/$', 'tracker.views.issue_unsubscribe', name='unsubscribe-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/add-label/(?P<label>[0-9]+)/$', 'tracker.views.issue_add_label', name='add-label-to-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/remove-label/(?P<label>[0-9]+)/$', 'tracker.views.issue_remove_label', name='remove-label-from-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/add-milestone/(?P<milestone>[a-z0-9_.-]+)/$', 'tracker.views.issue_add_milestone', name='add-milestone-to-issue'),
    url(r'^(?P<project>[-\w]+)/issues/(?P<issue>[0-9]+)/remove-milestone/(?P<milestone>[a-z0-9_.-]+)/$', 'tracker.views.issue_remove_milestone', name='remove-milestone-from-issue'),
    # Labels
    url(r'^(?P<project>[-\w]+)/labels/$', 'tracker.views.label_list', name='list-label'),
    url(r'^(?P<project>[-\w]+)/labels/add/$', 'tracker.views.label_edit', name='add-label'),
    url(r'^(?P<project>[-\w]+)/labels/(?P<id>[0-9]+)/edit/$', 'tracker.views.label_edit', name='edit-label'),
    url(r'^(?P<project>[-\w]+)/labels/(?P<id>[0-9]+)/delete/$', 'tracker.views.label_delete', name='delete-label'),
    # Milestones
    url(r'^(?P<project>[-\w]+)/milestones/$', 'tracker.views.milestone_list', name='list-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/add/$', 'tracker.views.milestone_edit', name='add-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/edit/$', 'tracker.views.milestone_edit', name='edit-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/close/$', 'tracker.views.milestone_close', name='close-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/reopen/$', 'tracker.views.milestone_reopen', name='reopen-milestone'),
    url(r'^(?P<project>[-\w]+)/milestones/(?P<name>[a-z0-9_.-]+)/delete/$', 'tracker.views.milestone_delete', name='delete-milestone'),
    # Activities
    url(r'^(?P<project>[-\w]+)/activity/$', 'tracker.views.activity', name='show-activity'),
    # Default redirection
    url(r'^(?P<project>[-\w]+)/$', 'tracker.views.project_redirect'),
]
