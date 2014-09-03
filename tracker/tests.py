from django.test import TestCase
from django.core.urlresolvers import reverse

from tracker.models import *
from accounts.models import User


class TestViews(TestCase):

    fixtures = ['test_tracker_views']

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_admin(self):
        response = self.client.get(reverse('admin'))
        self.assertRedirects(response, reverse('settings'))

    def test_settings(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

    # Projects

    def test_project_list(self):
        response = self.client.get(reverse('list-project'))
        self.assertEqual(response.status_code, 200)
        Project.objects.all().delete()
        response = self.client.get(reverse('list-project'))
        self.assertRedirects(response, reverse('add-project'))

    def test_project_add(self):
        response = self.client.get(reverse('add-project'))
        self.assertEqual(response.status_code, 200)

    def test_project_edit(self):
        project = Project.objects.first()
        response = self.client.get(reverse('edit-project', args=[project.name]))
        self.assertEqual(response.status_code, 200)

    def test_project_delete(self):
        project = Project.objects.first()
        response = self.client.get(reverse('delete-project', args=[project.name]))
        self.assertEqual(response.status_code, 405) # get method not allowed
        response = self.client.post(reverse('delete-project', args=[project.name]))
        self.assertRedirects(response, reverse('list-project'))

    def test_project_subscribe_unsubscribe(self):
        self.client.logout()
        self.client.login(username='user1', password='user1')
        user = User.objects.get(username='user1')
        project = Project.objects.get(name='project-1')
        self.assertFalse(user in project.subscribers.all())
        response = self.client.get(reverse('subscribe-project', args=[project.name]))
        self.assertRedirects(response, reverse('profile'))
        user.email = 'user@example.com'
        user.save()
        response = self.client.get(reverse('subscribe-project', args=[project.name]))
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertTrue(user in project.subscribers.all())
        response = self.client.get(reverse('unsubscribe-project', args=[project.name]))
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertFalse(user in project.subscribers.all())

    # Issue

    def test_issue_list(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('list-issue', args=[project.name]))
        self.assertEqual(response.status_code, 200)

    def test_issue_add(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('add-issue', args=[project.name]))
        self.assertEqual(response.status_code, 200)

    def test_issue_edit(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.first()
        response = self.client.get(reverse('edit-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)

    def test_issue_details(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='Issue 1')
        response = self.client.get(reverse('show-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)

    def test_issue_comment_add(self):
        pass

    def test_issue_comment_edit(self):
        pass

    def test_issue_comment_delete(self):
        pass

    def test_issue_close_reopen(self):
        issue = Issue.objects.filter(closed=False).first()
        project = issue.project
        response = self.client.get(reverse('reopen-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('close-issue', args=[project.name, issue.id]))
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertTrue(issue.closed)
        response = self.client.get(reverse('close-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('reopen-issue', args=[project.name, issue.id]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertFalse(issue.closed)

    def test_issue_delete(self):
        count = Issue.objects.count()
        issue = Issue.objects.first()
        project = issue.project
        response = self.client.get(reverse('delete-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 405) # get method forbidden
        response = self.client.post(reverse('delete-issue', args=[project.name, issue.id]))
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        self.assertEqual(Issue.objects.count(), count - 1)

    def test_issue_add_label(self):
        pass

    def test_issue_remove_label(self):
        pass

    def test_issue_add_milestone(self):
        pass

    def test_issue_remove_milestone(self):
        pass

    def test_issue_subscribe_unsubscribe(self):
        self.client.logout()
        self.client.login(username='user1', password='user1')
        user = User.objects.get(username='user1')
        issue = Issue.objects.get(title='Issue 1')
        project = issue.project
        self.assertFalse(user in issue.subscribers.all())
        response = self.client.get(reverse('subscribe-issue', args=[project.name, issue.id]))
        self.assertRedirects(response, reverse('profile'))
        user.email = 'user@example.com'
        user.save()
        response = self.client.get(reverse('subscribe-issue', args=[project.name, issue.id]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertTrue(user in issue.subscribers.all())
        response = self.client.get(reverse('unsubscribe-issue', args=[project.name, issue.id]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertFalse(user in issue.subscribers.all())

    # Labels

    def test_label_list(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('list-label', args=[project.name]))
        self.assertEqual(response.status_code, 200)

    def test_label_add(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('add-label', args=[project.name]))
        self.assertEqual(response.status_code, 200)

    def test_label_edit(self):
        project = Project.objects.get(name='project-1')
        label = project.labels.first()
        response = self.client.get(reverse('edit-label', args=[project.name, label.id]))
        self.assertEqual(response.status_code, 200)

    def test_label_delete(self):
        count_active = Label.objects.filter(deleted=False).count()
        count_deleted = Label.objects.filter(deleted=True).count()
        label = Label.objects.first()
        project = label.project
        response = self.client.get(reverse('delete-label', args=[project.name, label.id]))
        self.assertEqual(response.status_code, 405) # get method forbidden
        response = self.client.post(reverse('delete-label', args=[project.name, label.id]))
        self.assertRedirects(response, reverse('list-label', args=[project.name]))
        self.assertEqual(Label.objects.filter(deleted=False).count(), count_active - 1)
        self.assertEqual(Label.objects.filter(deleted=True).count(), count_deleted + 1)


    # Milestones

    def test_milestone_list(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('list-milestone', args=[project.name]))
        self.assertEqual(response.status_code, 200)

    def test_milestone_add(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('add-milestone', args=[project.name]))
        self.assertEqual(response.status_code, 200)

    def test_milestone_edit(self):
        project = Project.objects.get(name='project-1')
        milestone = project.milestones.first()
        response = self.client.get(reverse('edit-milestone', args=[project.name, milestone.name]))
        self.assertEqual(response.status_code, 200)

    def test_milestone_close_reopen(self):
        milestone = Milestone.objects.filter(closed=False).first()
        project = milestone.project
        response = self.client.get(reverse('reopen-milestone', args=[project.name, milestone.name]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('close-milestone', args=[project.name, milestone.name]))
        self.assertRedirects(response, reverse('list-milestone', args=[project.name]))
        milestone = Milestone.objects.get(pk=milestone.pk)
        self.assertTrue(milestone.closed)
        response = self.client.get(reverse('close-milestone', args=[project.name, milestone.name]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('reopen-milestone', args=[project.name, milestone.name]))
        self.assertRedirects(response, reverse('list-milestone', args=[project.name]))
        milestone = Milestone.objects.get(pk=milestone.pk)
        self.assertFalse(milestone.closed)

    def test_milestone_delete(self):
        count = Milestone.objects.count()
        project = Project.objects.get(name='project-1')
        milestone = project.milestones.first()
        response = self.client.get(reverse('delete-milestone', args=[project.name, milestone.name]))
        self.assertEqual(response.status_code, 405) # get method forbidden
        response = self.client.post(reverse('delete-milestone', args=[project.name, milestone.name]))
        self.assertRedirects(response, reverse('list-milestone', args=[project.name]))
        self.assertEqual(Milestone.objects.count(), count - 1)
