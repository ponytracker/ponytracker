from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from permissions.models import *
from permissions.models import PermissionModel as PermModel
from accounts.models import *
from tracker.models import *


class TestViews(TestCase):

    fixtures = ['test_permissions_views']

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_global_perm_list(self):
        response = self.client.get(reverse('list-global-permission'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create project")
        self.assertContains(response, "Access all project")

    def test_global_perm_add(self):
        count = GlobalPermission.objects.count()
        response = self.client.get(reverse('add-global-permission'))
        self.assertEqual(response.status_code, 200)
        # user
        response = self.client.post(reverse('add-global-permission'), {
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        user = User.objects.create(username='newuser')
        response = self.client.post(reverse('add-global-permission'), {
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': user.username,
        })
        self.assertRedirects(response, reverse('list-global-permission'))
        self.assertEqual(GlobalPermission.objects.count(), count + 1)
        # group
        response = self.client.post(reverse('add-global-permission'), {
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': 'newgroup',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        group = Group.objects.create(name='newgroup')
        response = self.client.post(reverse('add-global-permission'), {
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': group.name,
        })
        self.assertRedirects(response, reverse('list-global-permission'))
        self.assertEqual(GlobalPermission.objects.count(), count + 2)
        # team
        response = self.client.post(reverse('add-global-permission'), {
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': 'newteam',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        team = Team.objects.create(name='newteam')
        response = self.client.post(reverse('add-global-permission'), {
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': team.name,
        })
        self.assertRedirects(response, reverse('list-global-permission'))
        self.assertEqual(GlobalPermission.objects.count(), count + 3)

    def test_global_perm_edit(self):
        perm = GlobalPermission.objects.first()
        response = self.client.get(reverse('edit-global-permission', args=[perm.id]))
        self.assertEqual(response.status_code, 200)
        # user
        response = self.client.post(reverse('edit-global-permission', args=[perm.id]), {
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        user = User.objects.create(username='newuser')
        response = self.client.post(reverse('edit-global-permission', args=[perm.id]), {
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': user.username,
        })
        self.assertRedirects(response, reverse('list-global-permission'))
        perm = GlobalPermission.objects.get(pk=perm.pk)
        self.assertEqual(user, perm.grantee)
        # group
        response = self.client.post(reverse('edit-global-permission', args=[perm.id]), {
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': 'newgroup',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        group = Group.objects.create(name='newgroup')
        response = self.client.post(reverse('edit-global-permission', args=[perm.id]), {
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': group.name,
        })
        self.assertRedirects(response, reverse('list-global-permission'))
        perm = GlobalPermission.objects.get(pk=perm.pk)
        self.assertEqual(group, perm.grantee)
        # team
        response = self.client.post(reverse('edit-global-permission', args=[perm.id]), {
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': 'newteam',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        team = Team.objects.create(name='newteam')
        response = self.client.post(reverse('edit-global-permission', args=[perm.id]), {
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': team.name,
        })
        self.assertRedirects(response, reverse('list-global-permission'))
        perm = GlobalPermission.objects.get(pk=perm.pk)
        self.assertEqual(team, perm.grantee)

    def test_global_perm_delete(self):
        perm = GlobalPermission.objects.first()
        count = GlobalPermission.objects.count()
        response = self.client.get(reverse('delete-global-permission', args=[perm.id]))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse('delete-global-permission', args=[perm.id]))
        self.assertRedirects(response, reverse('list-global-permission'))
        self.assertEqual(GlobalPermission.objects.count(), count - 1)

    def test_global_perm_toggle(self):
        perm = GlobalPermission.objects.first()
        perm.create_project = True
        perm.save()
        response = self.client.get(reverse('toggle-global-permission', args=[perm.id, 'not_existing']))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('toggle-global-permission', args=[perm.id, 'create_project']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '0')
        perm = GlobalPermission.objects.get(pk=perm.pk)
        self.assertEqual(perm.create_project, False)
        response = self.client.get(reverse('toggle-global-permission', args=[perm.id, 'create_project']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '1')
        perm = GlobalPermission.objects.get(pk=perm.pk)
        self.assertEqual(perm.create_project, True)

    def test_project_perm_list(self):
        project = Project.objects.first()
        response = self.client.get(reverse('list-project-permission', args=[project.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create issue")

    def test_project_perm_add(self):
        project = Project.objects.get(name='project-1')
        wrongproject = Project.objects.get(name='project-2')
        count = project.permissions.count()
        response = self.client.get(reverse('add-project-permission', args=[project.name]))
        self.assertEqual(response.status_code, 200)
        # user
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        user = User.objects.create(username='newuser')
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': user.username,
        })
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertEqual(project.permissions.count(), count + 1)
        # group
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': 'newgroup',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        group = Group.objects.create(name='newgroup')
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': group.name,
        })
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertEqual(project.permissions.count(), count + 2)
        # team
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': 'newteam',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        team = Team.objects.create(name='newteam')
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': team.name,
        })
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertEqual(project.permissions.count(), count + 3)
        # wrong project
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': wrongproject.id,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('add-project-permission', args=[project.name]), {
            'project': 42,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 200)

    def test_project_perm_edit(self):
        project = Project.objects.get(name='project-1')
        wrongproject = Project.objects.get(name='project-2')
        perm = project.permissions.first()
        response = self.client.get(reverse('edit-project-permission', args=[project.name, perm.id]))
        self.assertEqual(response.status_code, 200)
        # user
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        user = User.objects.create(username='newuser')
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': user.username,
        })
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        perm = ProjectPermission.objects.get(pk=perm.pk)
        self.assertEqual(user, perm.grantee)
        # group
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': 'newgroup',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        group = Group.objects.create(name='newgroup')
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_GROUP,
            'grantee_id': 42,
            'grantee_name': group.name,
        })
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        perm = ProjectPermission.objects.get(pk=perm.pk)
        self.assertEqual(group, perm.grantee)
        # team
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': 'newteam',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exists')
        team = Team.objects.create(name='newteam')
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': project.id,
            'grantee_type': PermModel.GRANTEE_TEAM,
            'grantee_id': 42,
            'grantee_name': team.name,
        })
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        perm = ProjectPermission.objects.get(pk=perm.pk)
        self.assertEqual(team, perm.grantee)
        # wrong project
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': wrongproject.id,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('edit-project-permission', args=[project.name, perm.id]), {
            'project': 42,
            'grantee_type': PermModel.GRANTEE_USER,
            'grantee_id': 42,
            'grantee_name': 'newuser',
        })
        self.assertEqual(response.status_code, 200)

    def test_project_perm_delete(self):
        project = Project.objects.get(name='project-1')
        perm = project.permissions.first()
        count = project.permissions.count()
        ProjectPermission.objects.get(project=project, id=perm.id)
        response = self.client.get(reverse('delete-project-permission', args=[project.name, perm.id]))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse('delete-project-permission', args=[project.name, perm.id]))
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertEqual(project.permissions.count(), count - 1)

    def test_project_perm_toggle(self):
        project = Project.objects.get(name='project-1')
        perm = project.permissions.first()
        perm.create_issue = True
        perm.save()
        response = self.client.get(reverse('toggle-project-permission', args=[project.name, perm.id, 'not_existing']))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('toggle-project-permission', args=[project.name, perm.id, 'create_issue']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '0')
        perm = ProjectPermission.objects.get(pk=perm.pk)
        self.assertEqual(perm.create_issue, False)
        response = self.client.get(reverse('toggle-project-permission', args=[project.name, perm.id, 'create_issue']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '1')
        perm = ProjectPermission.objects.get(pk=perm.pk)
        self.assertEqual(perm.create_issue, True)

class TestGlobalPerm(TestCase):

    fixtures = ['test_permissions']

    def test_direct(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_USER,
                grantee_id=user.id,
                create_project=False,
                access_project=False)
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.create_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.access_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertTrue(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))

    def test_through_group(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        group = Group.objects.get(name='group')
        user.groups.add(group)
        user.save()
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_GROUP,
                grantee_id=group.id,
                create_project=False,
                access_project=False)
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.create_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.access_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertTrue(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))

    def test_through_team_direct(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        team = Team.objects.get(name='team')
        team.users.add(user)
        team.save()
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_TEAM,
                grantee_id=team.id,
                create_project=False,
                access_project=False)
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.create_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.access_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertTrue(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))

    def test_through_team_throught_group(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        group = Group.objects.get(name='group')
        team = Team.objects.get(name='team')
        user.groups.add(group)
        user.save()
        team.groups.add(group)
        team.save()
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_TEAM,
                grantee_id=team.id,
                create_project=False,
                access_project=False)
        self.assertFalse(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.create_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertFalse(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))
        perm.access_project = True
        perm.save()
        self.assertTrue(user.has_perm('create_project'))
        self.assertTrue(user.has_perm('access_project'))
        self.assertFalse(guess.has_perm('create_project'))


class TestProjectPerm(TestCase):

    fixtures = ['test_permissions']

    def test_direct(self):
        project1 = Project.objects.get(name='project-1')
        project2 = Project.objects.get(name='project-2')
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm = ProjectPermission.objects.create(
                project=project1,
                grantee_type=PermModel.GRANTEE_USER,
                grantee_id=user.id,
                create_issue=False,
                modify_issue=False)
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.create_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.modify_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertTrue(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))

    def test_through_group(self):
        project1 = Project.objects.get(name='project-1')
        project2 = Project.objects.get(name='project-2')
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        group = Group.objects.get(name='group')
        user.groups.add(group)
        user.save()
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm = ProjectPermission.objects.create(
                project=project1,
                grantee_type=PermModel.GRANTEE_GROUP,
                grantee_id=group.id,
                create_issue=False,
                modify_issue=False)
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.create_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.modify_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertTrue(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))


    def test_through_team_direct(self):
        project1 = Project.objects.get(name='project-1')
        project2 = Project.objects.get(name='project-2')
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        team = Team.objects.get(name='team')
        team.users.add(user)
        team.save()
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm = ProjectPermission.objects.create(
                project=project1,
                grantee_type=PermModel.GRANTEE_TEAM,
                grantee_id=team.id,
                create_issue=False,
                modify_issue=False)
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.create_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.modify_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertTrue(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))

    def test_through_team_throught_group(self):
        project1 = Project.objects.get(name='project-1')
        project2 = Project.objects.get(name='project-2')
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        group = Group.objects.get(name='group')
        team = Team.objects.get(name='team')
        user.groups.add(group)
        user.save()
        team.groups.add(group)
        team.save()
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm = ProjectPermission.objects.create(
                project=project1,
                grantee_type=PermModel.GRANTEE_TEAM,
                grantee_id=team.id,
                create_issue=False,
                modify_issue=False)
        self.assertFalse(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.create_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertFalse(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))
        perm.modify_issue = True
        perm.save()
        self.assertTrue(user.has_perm('create_issue', project1))
        self.assertTrue(user.has_perm('modify_issue', project1))
        self.assertFalse(user.has_perm('create_issue', project2))
        self.assertFalse(guess.has_perm('create_issue', project1))


class TestModels(TestCase):

    fixtures = ['test_permissions']

    def test_user(self):
        user = User.objects.first()
        perm = GlobalPermission()
        perm.grantee = user
        self.assertEqual(perm.grantee_type, PermModel.GRANTEE_USER)
        self.assertEqual(perm.grantee_id, user.id)

    def test_group(self):
        group = Group.objects.first()
        perm = GlobalPermission()
        perm.grantee = group
        self.assertEqual(perm.grantee_type, PermModel.GRANTEE_GROUP)
        self.assertEqual(perm.grantee_id, group.id)

    def test_team(self):
        team = Team.objects.first()
        perm = GlobalPermission()
        perm.grantee = team
        self.assertEqual(perm.grantee_type, PermModel.GRANTEE_TEAM)
        self.assertEqual(perm.grantee_id, team.id)

    def test_error(self):
        perm = GlobalPermission()
        def test():
            perm.grantee = "grantee"
        self.assertRaisesMessage(ValueError, 'Grantee object must be an User, a Group or a Team instance.', test)

    def test_broken(self):
        user = User.objects.get(username='user')
        perm = GlobalPermission() # not valid
        self.assertFalse(perm.granted_to(user))

    def test_direct(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_USER,
                grantee_id=user.id)
        self.assertTrue(perm.granted_to(user))
        self.assertFalse(perm.granted_to(guess))
        self.assertFalse(perm.granted_to(AnonymousUser()))

    def test_through_group(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        group = Group.objects.get(name='group')
        user.groups.add(group)
        user.save()
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_GROUP,
                grantee_id=group.id)
        self.assertTrue(perm.granted_to(user))
        self.assertFalse(perm.granted_to(guess))

    def test_through_team_direct(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        team = Team.objects.get(name='team')
        team.users.add(user)
        team.save()
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_TEAM,
                grantee_id=team.id)
        self.assertTrue(perm.granted_to(user))
        self.assertFalse(perm.granted_to(guess))

    def test_through_team_throught_group(self):
        user = User.objects.get(username='user')
        guess = User.objects.get(username='guess')
        group = Group.objects.get(name='group')
        team = Team.objects.get(name='team')
        user.groups.add(group)
        user.save()
        team.groups.add(group)
        team.save()
        perm = GlobalPermission.objects.create(
                grantee_type=PermModel.GRANTEE_TEAM,
                grantee_id=team.id)
        self.assertTrue(perm.granted_to(user))
        self.assertFalse(perm.granted_to(guess))
