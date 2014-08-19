from django.test import TestCase, Client
from django import VERSION

from issue.models import *


class TestPermissions(TestCase):

    fixtures = ['test_perms']

    def test_team_user_membership(self):
        user = User.objects.get(username='user1')
        team = Team.objects.get(name='team1')
        self.assertEqual(len(user.teams), 1)
        self.assertEqual(user.teams[0], team)

    def test_team_group_membership(self):
        user = User.objects.get(username='user2')
        team = Team.objects.get(name='team2')
        self.assertEqual(len(user.teams), 1)
        self.assertEqual(user.teams[0], team)

    def test_global_no_perms(self):
        user = User.objects.get(username='user4')
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('modify_project'))
        self.assertFalse(user.has_perm('delete_project'))

    def test_global_user_perms(self):
        user = User.objects.get(username='user3')
        self.assertTrue(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('modify_project'))
        self.assertFalse(user.has_perm('delete_project'))

    def test_global_group_perms(self):
        user = User.objects.get(username='user2')
        self.assertFalse(user.has_perm('create_project'))
        self.assertTrue(user.has_perm('modify_project'))
        self.assertFalse(user.has_perm('delete_project'))

    def test_global_team_perms(self):
        user = User.objects.get(username='user1')
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('modify_project'))
        self.assertTrue(user.has_perm('delete_project'))

    def test_project_no_perms(self):
        user = User.objects.get(username='user4')
        project = Project.objects.get(name='project-1')
        self.assertFalse(user.has_perm('create_issue', project))
        self.assertFalse(user.has_perm('modify_issue', project))
        self.assertFalse(user.has_perm('delete_issue', project))

    def test_project_user_perms(self):
        user = User.objects.get(username='user3')
        project = Project.objects.get(name='project-1')
        self.assertTrue(user.has_perm('create_issue', project))
        self.assertFalse(user.has_perm('modify_issue', project))
        self.assertFalse(user.has_perm('delete_issue', project))

    def test_project_group_perms(self):
        user = User.objects.get(username='user2')
        project = Project.objects.get(name='project-1')
        self.assertFalse(user.has_perm('create_issue', project))
        self.assertTrue(user.has_perm('modify_issue', project))
        self.assertFalse(user.has_perm('delete_issue', project))

    def test_project_team_perms(self):
        user = User.objects.get(username='user1')
        project = Project.objects.get(name='project-1')
        self.assertFalse(user.has_perm('create_issue', project))
        self.assertFalse(user.has_perm('modify_issue', project))
        self.assertTrue(user.has_perm('delete_issue', project))

    def test_unregistered_project_list(self):
        response = self.client.get('/')
        projects = response.context['projects']
        project = Project.objects.get(name='project-1')
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0], project)

    def test_ungranted_project_list(self):
        self.client.login(username='user1', password='user1')
        response = self.client.get('/')
        projects = response.context['projects']
        project = Project.objects.get(name='project-1')
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0], project)
        self.client.logout()

    def test_granted_project_list(self):
        self.client.login(username='user2', password='user2')
        response = self.client.get('/')
        projects = response.context['projects']
        project1 = Project.objects.get(name='project-1')
        project2 = Project.objects.get(name='project-2')
        self.assertEqual(len(projects), 2)
        self.assertTrue(project1 in projects)
        self.assertTrue(project2 in projects)


class TestNoProject(TestCase):

    fixtures = ['test_no_project']

    def test_ano(self):
        url = reverse('list-project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There is not any public project')

    def test_without_add_permission(self):
        self.client.login(username='user1', password='user1')
        url = reverse('list-project')
        expected_url = reverse('add-project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                'Sorry, you have no access to any project')

    def test_with_add_permission(self):
        self.client.login(username='user2', password='user2')
        url = reverse('list-project')
        expected_url = reverse('add-project')
        response = self.client.get(url)
        if VERSION >= (1, 7):
            self.assertRedirects(response, expected_url,
                    # don't fetch redirect to don't loose message
                    fetch_redirect_response=False)
            response = self.client.get(expected_url)
            self.assertContains(response, 'Start by creating a project')
        else:
            self.assertRedirects(response, expected_url)


class TestGlobalViews(TestCase):

    fixtures = ['test_perms']

    def test_404(self):
        response = self.client.get('/deliberately/broken')
        self.assertEqual(response.status_code, 404)

    def test_profile_ano(self):
        url = reverse('profile')
        expected_url = reverse('login') + '?next=' + url
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)

    def test_profile_user1(self):
        self.client.login(username='user1', password='user1')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'group1')
        self.assertContains(response, 'team1')
        self.assertNotContains(response, 'team2')

    def test_profile_user2(self):
        self.client.login(username='user2', password='user2')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'group1')
        self.assertNotContains(response, 'team1')
        self.assertContains(response, 'team2')


class TestProjectsViews(TestCase):

    fixtures = ['test_perms']

    def test_home_as_anonymous(self):
        expected = Project.objects.filter(name='project-1')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'],
                lambda x: x)

    def test_home_as_user1(self):
        expected = Project.objects.filter(name='project-1')
        self.client.login(username='user1', password='user1')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'],
                lambda x: x, ordered=False)
        self.assertNotContains(response, 'New project')

    def test_home_as_user2(self):
        expected = Project.objects.all()
        self.client.login(username='user2', password='user2')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'],
                lambda x: x, ordered=False)
        self.assertNotContains(response, 'New project')

    def test_home_as_user3(self):
        expected = Project.objects.filter(name='project-1')
        self.client.login(username='user3', password='user3')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'],
                lambda x: x, ordered=False)
        self.assertContains(response, 'New project')

    def test_home_as_admin(self):
        expected = Project.objects.all()
        self.client.login(username='admin', password='admin')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'],
                lambda x: x, ordered=False)
        self.assertContains(response, 'New project')

    def test_add_project_granted(self):
        self.client.login(username='user3', password='user3')
        expected_url = reverse('list-project-permission', args=['project-3'])
        url = reverse('add-project')
        response = self.client.post(url, {
            'name': 'project-3',
            'display_name': 'Project 3',
            'description': 'This is the third project.',
        })
        self.assertRedirects(response, expected_url)
        self.assertQuerysetEqual(Project.objects.all(),
            ['project-1', 'project-2', 'project-3'],
            lambda x: x.name, ordered=False)

    def test_add_project_forbidden(self):
        self.client.login(username='user1', password='user1')
        url = reverse('add-project')
        response = self.client.post(url, {
            'name': 'project-3',
            'display_name': 'Project 3',
            'description': 'This is the third project.',
        })
        self.assertEqual(response.status_code, 403)
        self.assertQuerysetEqual(Project.objects.all(),
                ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_add_project_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' + reverse('add-project')
        url = reverse('add-project')
        response = self.client.post(url, {
            'name': 'project-3',
            'display_name': 'Project 3',
            'description': 'This is the third project.',
        })
        self.assertRedirects(response, expected_url)
        self.assertQuerysetEqual(Project.objects.all(),
            ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_delete_project_get(self):
        self.client.login(username='user1', password='user1')
        expected_url = reverse('list-project')
        url = reverse('delete-project', args=['project-1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        self.assertQuerysetEqual(Project.objects.all(),
            ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_delete_project_granted(self):
        self.client.login(username='user1', password='user1')
        expected_url = reverse('list-project')
        url = reverse('delete-project', args=['project-1'])
        response = self.client.post(url)
        self.assertRedirects(response, expected_url)
        self.assertQuerysetEqual(Project.objects.all(),
            ['project-2'], lambda x: x.name, ordered=False)

    def test_delete_project_forbidden(self):
        self.client.login(username='user2', password='user2')
        url = reverse('delete-project', args=['project-1'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertQuerysetEqual(Project.objects.all(),
            ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_delete_project_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' \
            + reverse('delete-project', args=['project-1'])
        url = reverse('delete-project', args=['project-1'])
        response = self.client.post(url)
        self.assertRedirects(response, expected_url)
        self.assertQuerysetEqual(Project.objects.all(),
            ['project-1', 'project-2'], lambda x: x.name, ordered=False)


class TestIssuesViews(TestCase):

    fixtures = ['test_perms']

    def test_list_issue_granted(self):
        self.client.login(username='user2', password='user2')
        url = reverse('list-issue', args=['project-2'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_issue_forbidden(self):
        self.client.login(username='user1', password='user1')
        expected_url = reverse('login') + '?next=' \
            + reverse('list-issue', args=['project-2'])
        url = reverse('list-issue', args=['project-2'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_list_issue_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' \
            + reverse('list-issue', args=['project-2'])
        url = reverse('list-issue', args=['project-2'])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)

    def test_show_issue_granted(self):
        self.client.login(username='user2', password='user2')
        url = reverse('show-issue', args=['project-2', 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_show_issue_granted_ano(self):
        url = reverse('show-issue', args=['project-1', 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_show_issue_forbidden(self):
        self.client.login(username='user1', password='user1')
        expected_url = reverse('login') + '?next=' \
            + reverse('show-issue', args=['project-2', 1])
        url = reverse('show-issue', args=['project-2', 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_add_issue_granted(self):
        self.client.login(username='user5', password='user5')
        expected_url = reverse('show-issue', args=['project-2', 3])
        url = reverse('add-issue', args=['project-2'])
        response = self.client.post(url, {
            'title': 'Issue 3',
            'description': 'This is the third issue.',
        })
        self.assertRedirects(response, expected_url)
        issues = Issue.objects.filter(project__name='project-2')
        self.assertQuerysetEqual(issues, ['Issue 1', 'Issue 2', 'Issue 3'],
                lambda x: x.title, ordered=False)

    def test_add_issue_forbidden(self):
        self.client.login(username='user6', password='user6')
        url = reverse('add-issue', args=['project-2'])
        response = self.client.post(url, {
            'title': 'Issue 3',
            'description': 'This is the third issue.',
        })
        self.assertEqual(response.status_code, 403)
        issues = Issue.objects.filter(project__name='project-2')
        self.assertQuerysetEqual(issues, ['Issue 1', 'Issue 2'],
                lambda x: x.title, ordered=False)

    def test_add_issue_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' \
            + reverse('add-issue', args=['project-2'])
        url = reverse('add-issue', args=['project-2'])
        response = self.client.post(url, {
            'title': 'Issue 3',
            'description': 'This is the third issue.',
        })
        self.assertRedirects(response, expected_url)
        issues = Issue.objects.filter(project__name='project-2')
        self.assertQuerysetEqual(issues, ['Issue 1', 'Issue 2'],
                lambda x: x.title, ordered=False)

    def test_delete_issue_get(self):
        self.client.login(username='user8', password='user8')
        expected_url = reverse('list-issue', args=['project-2'])
        url = reverse('delete-issue', args=['project-2', 2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        issues = Issue.objects.filter(project__name='project-2')
        self.assertQuerysetEqual(issues, ['Issue 1', 'Issue 2'],
                lambda x: x.title, ordered=False)

    def test_delete_issue_granted(self):
        self.client.login(username='user8', password='user8')
        expected_url = reverse('list-issue', args=['project-2'])
        url = reverse('delete-issue', args=['project-2', 2])
        response = self.client.post(url)
        self.assertRedirects(response, expected_url)
        issues = Issue.objects.filter(project__name='project-2')
        self.assertQuerysetEqual(issues, ['Issue 1'],
                lambda x: x.title, ordered=False)

    def test_delete_issue_forbidden(self):
        self.client.login(username='user5', password='user5')
        url = reverse('delete-issue', args=['project-2', 2])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        issues = Issue.objects.filter(project__name='project-2')
        self.assertQuerysetEqual(issues, ['Issue 1', 'Issue 2'],
                lambda x: x.title, ordered=False)

    def test_delete_issue_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' \
            + reverse('delete-issue', args=['project-2', 2])
        url = reverse('delete-issue', args=['project-2', 2])
        response = self.client.post(url)
        self.assertRedirects(response, expected_url)
        issues = Issue.objects.filter(project__name='project-2')
        self.assertQuerysetEqual(issues, ['Issue 1', 'Issue 2'],
                lambda x: x.title, ordered=False)

    def test_close_issue_granted(self):
        self.client.login(username='user6', password='user6')
        expected_url = reverse('list-issue', args=['project-2'])
        url = reverse('close-issue', args=['project-2', 1])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=1)
        self.assertEqual(issue.closed, True)

    def test_close_issue_forbidden(self):
        self.client.login(username='user5', password='user5')
        url = reverse('close-issue', args=['project-2', 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        issue = Issue.objects.get(project__name='project-2', id=1)
        self.assertEqual(issue.closed, False)

    def test_close_issue_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' \
            + reverse('close-issue', args=['project-2', 1])
        url = reverse('close-issue', args=['project-2', 1])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=1)
        self.assertEqual(issue.closed, False)

    def test_reopen_issue_granted(self):
        self.client.login(username='user6', password='user6')
        expected_url = reverse('show-issue', args=['project-2', 2])
        url = reverse('reopen-issue', args=['project-2', 2])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=2)
        self.assertEqual(issue.closed, False)

    def test_reopen_issue_forbidden(self):
        self.client.login(username='user5', password='user5')
        url = reverse('reopen-issue', args=['project-2', 2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        issue = Issue.objects.get(project__name='project-2', id=2)
        self.assertEqual(issue.closed, True)

    def test_reopen_issue_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' \
            + reverse('reopen-issue', args=['project-2', 2])
        url = reverse('reopen-issue', args=['project-2', 2])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=2)
        self.assertEqual(issue.closed, True)

    def test_modify_issue_granted(self):
        self.client.login(username='user7', password='user7')
        expected_url = reverse('show-issue', args=['project-2', 1])
        url = reverse('edit-issue', args=['project-2', 1])
        response = self.client.post(url, {
            'title': '*THE* Issue 1',
            'description': 'This is *THE* first issue.',
        })
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=1)
        self.assertEqual(issue.title, "*THE* Issue 1")
        self.assertEqual(issue.description, "This is *THE* first issue.")

    def test_modify_issue_forbidden(self):
        self.client.login(username='user5', password='user5')
        url = reverse('edit-issue', args=['project-2', 1])
        response = self.client.post(url, {
            'title': '*THE* Issue 1',
            'description': 'This is *THE* first issue.',
        })
        self.assertEqual(response.status_code, 403)
        issue = Issue.objects.get(project__name='project-2', id=1)
        self.assertEqual(issue.title, "Issue 1")
        self.assertEqual(issue.description, "This is the first issue.")

    def test_modify_issue_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' \
            + reverse('edit-issue', args=['project-2', 1])
        url = reverse('edit-issue', args=['project-2', 1])
        response = self.client.post(url, {
            'title': '*THE* Issue 1',
            'description': 'This is *THE* first issue.',
        })
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=1)
        self.assertEqual(issue.title, "Issue 1")
        self.assertEqual(issue.description, "This is the first issue.")


class TestComments(TestCase):

    fixtures = ['test_perms']

    def test_comment_issue_granted(self):
        self.client.login(username='user9', password='user9')
        msg = 'I have a lot to say.'
        expected_url = reverse('show-issue', args=['project-2', 1])
        url = reverse('comment-issue', args=['project-2', 1])
        response = self.client.post(url, {
            'comment': msg,
        })
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        self.assertEqual(event.additionnal_section, msg)

    def test_comment_issue_forbidden(self):
        self.client.login(username='user10', password='user10')
        msg = 'I have a lot to say.'
        url = reverse('comment-issue', args=['project-2', 1])
        response = self.client.post(url, {
            'comment': msg,
        })
        self.assertEqual(response.status_code, 403)
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        self.assertEqual(event.additionnal_section, 'Missing things')

    def test_edit_comment_granted(self):
        self.client.login(username='user10', password='user10')
        msg = 'Missing a lot of things'
        expected_url = reverse('show-issue', args=['project-2', 1])
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        url = reverse('edit-comment', args=['project-2', issue.id, event.id])
        response = self.client.post(url, {
            'comment': msg,
        })
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        self.assertEqual(event.additionnal_section, msg)

    def test_edit_comment_forbidden(self):
        self.client.login(username='user9', password='user9')
        msg = 'Missing a lot of things'
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        url = reverse('edit-comment', args=['project-2', issue.id, event.id])
        response = self.client.post(url, {
            'comment': msg,
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_comment_granted_get(self):
        self.client.login(username='user11', password='user11')
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        url = reverse('delete-comment', args=['project-2', issue.id, event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        self.assertEqual(event.additionnal_section, 'Missing things')

    def test_delete_comment_granted(self):
        self.client.login(username='user11', password='user11')
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        url = reverse('delete-comment', args=['project-2', issue.id, event.id])
        expected_url = reverse('show-issue', args=['project-2', 1])
        response = self.client.post(url)
        self.assertRedirects(response, expected_url)
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        self.assertEqual(event.additionnal_section, 'Done')

    def test_delete_comment_forbidden(self):
        self.client.login(username='user9', password='user9')
        msg = 'Missing a lot of things'
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        url = reverse('delete-comment', args=['project-2', issue.id, event.id])
        response = self.client.post(url, {
            'comment': msg,
        })
        self.assertEqual(response.status_code, 403)
        issue = Issue.objects.get(project__name='project-2', id=1)
        event = Event.objects.filter(issue=issue, code=Event.COMMENT).last()
        self.assertEqual(event.additionnal_section, 'Missing things')
