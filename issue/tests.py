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
