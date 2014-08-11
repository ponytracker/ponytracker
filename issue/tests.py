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

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_404(self):
        response = self.client.get('/deliberately/broken')
        self.assertEqual(response.status_code, 404)

    def test_home(self):
        url = reverse('list-project')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['projects']), 2)

    def test_home_redirection(self):
        Project.objects.all().delete()
        expected_url = reverse('add-project')
        url = reverse('list-project')
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)

    def test_add_project(self):
        expected_url = reverse('list-project-permission', args=['test'])
        url = reverse('add-project')
        response = self.client.post(url, {
            'name': 'test',
            'display_name': 'Test',
            'description': 'Testing purpose only.',
        })
        self.assertRedirects(response, expected_url)
        self.assertEqual(Project.objects.count(), 3)

    def test_delete_project(self):
        expected_url = reverse('list-project')
        url = reverse('delete-project', args=['project-1'])
        response = self.client.get(url)
        self.assertRedirects(response, expected_url)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().name, 'project-2')
