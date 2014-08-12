from django.test import TestCase, Client

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


class TestViews(TestCase):

    fixtures = ['test_perms']

    def test_404(self):
        response = self.client.get('/deliberately/broken')
        self.assertEqual(response.status_code, 404)

    def test_home_as_anonymous(self):
        expected = Project.objects.filter(name='project-1')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'], lambda x: x)

    def test_home_as_user1(self):
        expected = Project.objects.filter(name='project-1')
        self.client.login(username='user1', password='user1')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'], lambda x: x, ordered=False)
        self.assertNotContains(response, 'New project')

    def test_home_as_user2(self):
        expected = Project.objects.all()
        self.client.login(username='user2', password='user2')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'], lambda x: x, ordered=False)
        self.assertNotContains(response, 'New project')

    def test_home_as_user3(self):
        expected = Project.objects.filter(name='project-1')
        self.client.login(username='user3', password='user3')
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(expected, response.context['projects'], lambda x: x, ordered=False)
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
        self.assertQuerysetEqual(Project.objects.all(), ['project-1', 'project-2', 'project-3'], lambda x: x.name, ordered=False)

    def test_add_project_forbidden(self):
        self.client.login(username='user1', password='user1')
        url = reverse('add-project')
        response = self.client.post(url, {
            'name': 'project-3',
            'display_name': 'Project 3',
            'description': 'This is the third project.',
        })
        self.assertEqual(response.status_code, 403)
        self.assertQuerysetEqual(Project.objects.all(), ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_add_project_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' + reverse('add-project')
        url = reverse('add-project')
        response = self.client.post(url, {
            'name': 'project-3',
            'display_name': 'Project 3',
            'description': 'This is the third project.',
        })
        self.assertRedirects(response, expected_url)
        self.assertQuerysetEqual(Project.objects.all(), ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_delete_project_granted(self):
        self.client.login(username='user1', password='user1')
        expected_url = reverse('list-project')
        url = reverse('delete-project', args=['project-1'])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
        self.assertQuerysetEqual(Project.objects.all(), ['project-2'], lambda x: x.name, ordered=False)

    def test_delete_project_forbidden(self):
        self.client.login(username='user2', password='user2')
        url = reverse('delete-project', args=['project-1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertQuerysetEqual(Project.objects.all(), ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_delete_project_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' + reverse('delete-project', args=['project-1'])
        url = reverse('delete-project', args=['project-1'])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
        self.assertQuerysetEqual(Project.objects.all(), ['project-1', 'project-2'], lambda x: x.name, ordered=False)

    def test_list_issue_granted(self):
        self.client.login(username='user2', password='user2')
        url = reverse('list-issue', args=['project-2'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_issue_forbidden(self):
        self.client.login(username='user1', password='user1')
        expected_url = reverse('login') + '?next=' + reverse('list-issue', args=['project-2'])
        url = reverse('list-issue', args=['project-2'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_list_issue_forbidden_ano(self):
        expected_url = reverse('login') + '?next=' + reverse('list-issue', args=['project-2'])
        url = reverse('list-issue', args=['project-2'])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
