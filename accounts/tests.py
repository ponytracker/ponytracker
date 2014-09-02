import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from accounts.models import *


class TestViews(TestCase):

    fixtures = ['test_views']

    def setUp(self):
        self.client.login(username='admin', password='admin')

    # Profile

    def test_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    # Users

    def test_user_list(self):
        response = self.client.get(reverse('list-user'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1")
        self.assertContains(response, "Firstname1 Lastname1")

    def test_user_details(self):
        user = User.objects.get(username="user1")
        response = self.client.get(reverse('show-user', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1")
        self.assertContains(response, "group1")
        self.assertContains(response, "team1")

    def test_user_add(self):
        user_count = User.objects.count()
        response = self.client.post(reverse('add-user'), {
            'username': 'newuser',
        })
        self.assertEqual(User.objects.count(), user_count + 1)
        user = User.objects.get(username='newuser')
        self.assertRedirects(response, reverse('show-user', args=[user.id]))

    def test_user_edit(self):
        user = User.objects.get(username='user1')
        response = self.client.post(reverse('edit-user', args=[user.id]), {
            'first_name': 'newfirstname',
        })
        self.assertRedirects(response, reverse('show-user', args=[user.id]))
        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.first_name, 'newfirstname')

    def test_user_disable_activate(self):
        user = User.objects.get(username='user1')
        response = self.client.get(reverse('disable-user', args=[user.id]))
        self.assertRedirects(response, reverse('show-user', args=[user.id]))
        user = User.objects.get(pk=user.pk)
        self.assertFalse(user.is_active)
        response = self.client.get(reverse('activate-user', args=[user.id]))
        self.assertRedirects(response, reverse('show-user', args=[user.id]))
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.is_active)

    def test_user_edit_password(self):
        user = User.objects.get(username='user1')
        self.assertTrue(user.check_password("user1"))
        response = self.client.post(reverse('edit-user-password', args=[user.id]), {
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertRedirects(response, reverse('show-user', args=[user.id]))
        user = User.objects.get(username='user1')
        self.assertTrue(user.check_password('newpassword'))

    def test_user_delete_get(self):
        user_count = User.objects.count()
        user = User.objects.get(username='user1')
        response = self.client.get(reverse('delete-user', args=[user.id]))
        self.assertEqual(response.status_code, 405) # method not allowed
        self.assertEqual(User.objects.count(), user_count)

    def test_user_delete_post(self):
        user_count = User.objects.count()
        user = User.objects.get(username='user1')
        response = self.client.post(reverse('delete-user', args=[user.id]))
        self.assertRedirects(response, reverse('list-user'))
        self.assertEqual(User.objects.count(), user_count - 1)

    def test_user_add_group(self):
        user = User.objects.get(username='user1')
        group = Group.objects.create(name='newgroup')
        response = self.client.get(reverse('add-group-to-user', args=[user.id]) + '?term=new')
        self.assertEqual(response.status_code, 200)
        available = json.loads(response.content.decode('utf-8'))
        name = available[0]['value']
        response = self.client.post(reverse('add-group-to-user', args=[user.id]), {
            'group': name,
        })
        self.assertRedirects(response, reverse('show-user', args=[user.id]))
        user = User.objects.get(pk=user.pk)
        self.assertTrue(group in user.groups.all())

    def test_user_remove_group(self):
        user = User.objects.get(username='user1')
        group = user.groups.first()
        response = self.client.get(reverse('remove-group-from-user', args=[user.id, group.id]))
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(pk=user.pk)
        self.assertFalse(group in user.groups.all())

    def test_user_add_team(self):
        user = User.objects.get(username='user1')
        team = Team.objects.create(name='newteam')
        response = self.client.get(reverse('add-team-to-user', args=[user.id]) + '?term=new')
        self.assertEqual(response.status_code, 200)
        available = json.loads(response.content.decode('utf-8'))
        name = available[0]['value']
        response = self.client.post(reverse('add-team-to-user', args=[user.id]), {
            'team': name,
        })
        self.assertRedirects(response, reverse('show-user', args=[user.id]))
        team = Team.objects.get(pk=team.pk)
        self.assertTrue(user in team.users.all())

    def test_user_remove_team(self):
        user = User.objects.get(username='user1')
        team = user.teams.first()
        response = self.client.get(reverse('remove-team-from-user', args=[user.id, team.id]))
        self.assertEqual(response.status_code, 200)
        team = Team.objects.get(pk=team.pk)
        self.assertFalse(user in team.users.all())

    # Group

    def test_group_list(self):
        response = self.client.get(reverse('list-group'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "group1")

    def test_group_details(self):
        group = Group.objects.get(name="group1")
        response = self.client.get(reverse('show-group', args=[group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1")

    def test_group_add(self):
        group_count = Group.objects.count()
        response = self.client.post(reverse('add-group'), {
            'name': 'newgroup',
        })
        self.assertEqual(Group.objects.count(), group_count + 1)
        group = Group.objects.get(name='newgroup')
        self.assertRedirects(response, reverse('show-group', args=[group.id]))

    def test_group_edit(self):
        group = Group.objects.get(name='group1')
        response = self.client.post(reverse('edit-group', args=[group.id]), {
            'name': 'newname',
        })
        self.assertRedirects(response, reverse('show-group', args=[group.id]))
        group = Group.objects.get(pk=group.pk)
        self.assertEqual(group.name, 'newname')

    def test_group_delete_get(self):
        group_count = Group.objects.count()
        group = Group.objects.get(name='group1')
        response = self.client.get(reverse('delete-group', args=[group.id]))
        self.assertEqual(response.status_code, 405) # method not allowed
        self.assertEqual(Group.objects.count(), group_count)

    def test_group_delete_post(self):
        group_count = Group.objects.count()
        group = Group.objects.get(name='group1')
        response = self.client.post(reverse('delete-group', args=[group.id]))
        self.assertRedirects(response, reverse('list-group'))
        self.assertEqual(Group.objects.count(), group_count - 1)

    def test_group_add_user(self):
        group = Group.objects.get(name='group1')
        user = User.objects.create(username='newuser')
        response = self.client.get(reverse('add-user-to-group', args=[group.id]) + '?term=new')
        self.assertEqual(response.status_code, 200)
        available = json.loads(response.content.decode('utf-8'))
        name = available[0]['value']
        response = self.client.post(reverse('add-user-to-group', args=[group.id]), {
            'user': name,
        })
        self.assertRedirects(response, reverse('show-group', args=[group.id]))
        user = User.objects.get(pk=user.pk)
        self.assertTrue(group in user.groups.all())

    def test_group_remove_user(self):
        user = User.objects.get(username='user1')
        group = user.groups.first()
        response = self.client.get(reverse('remove-user-from-group', args=[group.id, user.id]))
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(pk=user.pk)
        self.assertFalse(group in user.groups.all())

    # Team

    def test_team_list(self):
        response = self.client.get(reverse('list-team'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'team1')
        self.assertContains(response, 'team2')

    def test_team_details(self):
        team = Team.objects.get(name="team2")
        response = self.client.get(reverse('show-team', args=[team.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user2")
        self.assertContains(response, "group2")

    def test_team_add(self):
        team_count = Team.objects.count()
        response = self.client.post(reverse('add-team'), {
            'name': 'newteam',
        })
        self.assertEqual(Team.objects.count(), team_count + 1)
        team = Team.objects.get(name='newteam')
        self.assertRedirects(response, reverse('show-team', args=[team.id]))

    def test_team_edit(self):
        team = Team.objects.get(name='team1')
        response = self.client.post(reverse('edit-team', args=[team.id]), {
            'name': 'newname',
        })
        self.assertRedirects(response, reverse('show-team', args=[team.id]))
        team = Team.objects.get(pk=team.pk)
        self.assertEqual(team.name, 'newname')

    def test_team_delete_get(self):
        team_count = Team.objects.count()
        team = Team.objects.get(name='team1')
        response = self.client.get(reverse('delete-team', args=[team.id]))
        self.assertEqual(response.status_code, 405) # method not allowed
        self.assertEqual(Team.objects.count(), team_count)

    def test_team_delete_post(self):
        team_count = Team.objects.count()
        team = Team.objects.get(name='team1')
        response = self.client.post(reverse('delete-team', args=[team.id]))
        self.assertRedirects(response, reverse('list-team'))
        self.assertEqual(Team.objects.count(), team_count - 1)

    def test_team_add_user(self):
        team = Team.objects.get(name='team2')
        user = User.objects.create(username='newuser')
        response = self.client.get(reverse('add-user-to-team', args=[team.id]) + '?term=new')
        self.assertEqual(response.status_code, 200)
        available = json.loads(response.content.decode('utf-8'))
        name = available[0]['value']
        response = self.client.post(reverse('add-user-to-team', args=[team.id]), {
            'user': name,
        })
        self.assertRedirects(response, reverse('show-team', args=[team.id]))
        team = Team.objects.get(pk=team.pk)
        self.assertTrue(user in team.users.all())

    def test_team_remove_user(self):
        team = Team.objects.get(name='team2')
        user = team.users.first()
        response = self.client.get(reverse('remove-user-from-team', args=[team.id, user.id]))
        self.assertEqual(response.status_code, 200)
        team = Team.objects.get(pk=team.pk)
        self.assertFalse(user in team.users.all())

    def test_team_add_group(self):
        team = Team.objects.get(name='team2')
        group = Group.objects.create(name='newgroup')
        response = self.client.get(reverse('add-group-to-team', args=[team.id]) + '?term=new')
        self.assertEqual(response.status_code, 200)
        available = json.loads(response.content.decode('utf-8'))
        name = available[0]['value']
        response = self.client.post(reverse('add-group-to-team', args=[team.id]), {
            'group': name,
        })
        self.assertRedirects(response, reverse('show-team', args=[team.id]))
        team = Team.objects.get(pk=team.pk)
        self.assertTrue(group in team.groups.all())

    def test_team_remove_group(self):
        team = Team.objects.get(name='team2')
        group = team.groups.first()
        response = self.client.get(reverse('remove-group-from-team', args=[team.id, group.id]))
        self.assertEqual(response.status_code, 200)
        team = Team.objects.get(pk=team.pk)
        self.assertFalse(group in team.groups.all())
