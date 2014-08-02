from django.conf.urls import url 

urlpatterns = [
    url(r'^$', 'issue.views.project_list', name='list-project'),
    url(r'^add$', 'issue.views.project_edit', name='add-project'),
    url(r'^(?P<project>[a-z0-9]+)/edit$', 'issue.views.project_edit', name='edit-project'),
    url(r'^(?P<project>[a-z0-9]+)/delete$', 'issue.views.project_delete', name='delete-project'),
    url(r'^(?P<project>[a-z0-9]+)/issues$', 'issue.views.issue_list', name='list-issue'),
    url(r'^(?P<project>[a-z0-9]+)/issues/add$', 'issue.views.issue_edit', name='add-issue'),
    url(r'^(?P<project>[a-z0-9]+)/issues/(?P<id>[0-9]+)$', 'issue.views.issue', name='show-issue'),
    url(r'^(?P<project>[a-z0-9]+)/issues/(?P<id>[0-9]+)/edit$', 'issue.views.issue_edit', name='edit-issue'),
    url(r'^(?P<project>[a-z0-9]+)/issues/(?P<id>[0-9]+)/close$', 'issue.views.issue_close', name='close-issue'),
    url(r'^(?P<project>[a-z0-9]+)/issues/(?P<id>[0-9]+)/reopen$', 'issue.views.issue_reopen', name='reopen-issue'),
    url(r'^(?P<project>[a-z0-9]+)/issues/(?P<id>[0-9]+)/comment$', 'issue.views.issue_comment', name='comment-issue'),
    url(r'^(?P<project>[a-z0-9]+)/issues/(?P<id>[0-9]+)/delete$', 'issue.views.issue_delete', name='delete-issue'),
    url(r'^(?P<project>[a-z0-9]+)/labels$', 'issue.views.label_list', name='list-label'),
    url(r'^(?P<project>[a-z0-9]+)/labels/add$', 'issue.views.label_edit', name='add-label'),
    url(r'^(?P<project>[a-z0-9]+)/labels/edit/(?P<id>[0-9]+)$', 'issue.views.label_edit', name='edit-label'),
    url(r'^(?P<project>[a-z0-9]+)/milestones$', 'issue.views.milestone_list', name='list-milestone'),
    url(r'^(?P<project>[a-z0-9]+)/milestones/add$', 'issue.views.milestone_edit', name='add-milestone'),
    url(r'^(?P<project>[a-z0-9]+)/milestones/edit/(?P<id>[0-9]+)$', 'issue.views.milestone_edit', name='edit-milestone'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
]
