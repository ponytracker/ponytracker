from django.test import TestCase
from django.core.urlresolvers import reverse

from tracker.models import *
from accounts.models import User
from permissions.models import PermissionModel as PermModel


class TestViews(TestCase):

    fixtures = ['test_tracker_views']

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_markdown(self):
        response = self.client.get(reverse('markdown'))
        self.assertEqual(response.status_code, 405) # get method not allowed
        response = self.client.post(reverse('markdown'), {
            'data': '**bold**',
        })
        self.assertContains(response, '<strong>bold</strong>')
        response = self.client.post(reverse('markdown'), {
            'data': '<script></script>',
        })
        self.assertNotContains(response, '<script>')

    def test_admin(self):
        response = self.client.get(reverse('admin'))
        self.assertRedirects(response, reverse('settings'))
        self.client.logout()
        response = self.client.get(reverse('admin'))
        self.assertRedirects(response, reverse('login')+'?next='+reverse('admin'))
        self.client.login(username='user1', password='user1')
        response = self.client.get(reverse('admin'))
        self.assertEqual(response.status_code, 403)

    def test_settings(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse('settings'))
        self.assertRedirects(response, reverse('login')+'?next='+reverse('settings'))
        self.client.login(username='user1', password='user1')
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 403)

    # Projects

    def test_project_list(self):
        response = self.client.get(reverse('list-project'))
        self.assertEqual(response.status_code, 200)
        Project.objects.all().delete()
        response = self.client.get(reverse('list-project'))
        self.assertRedirects(response, reverse('add-project'))
        self.client.logout()
        response = self.client.get(reverse('list-project'))
        self.assertEqual(response.status_code, 200)

    def test_project_add(self):
        count = Project.objects.count()
        response = self.client.get(reverse('add-project'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add-project'), {
            'display_name': 'project 1', # Project 1 already exist
            'name': 'newproject',
            'description': '',
            'access': Project.ACCESS_PUBLIC,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already a project')
        response = self.client.post(reverse('add-project'), {
            'display_name': 'New project',
            'name': 'admin', # reserved name
            'description': '',
            'access': Project.ACCESS_PUBLIC,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'this URL is reserved')
        response = self.client.post(reverse('add-project'), {
            'display_name': 'New project',
            'name': 'newproject',
            'description': '',
            'access': Project.ACCESS_PUBLIC,
        })
        self.assertEqual(Project.objects.count(), count + 1)
        project = Project.objects.get(name='newproject')
        self.assertRedirects(response, reverse('list-project-permission', args=[project.name]))
        self.assertEqual(project.permissions.count(), 1)
        perm = project.permissions.first()
        self.assertEqual(perm.grantee_type, PermModel.GRANTEE_USER)
        user = User.objects.get(username='admin')
        self.assertEqual(perm.grantee_id, user.id)

    def test_project_edit(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('edit-project', args=[project.name]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit-project', args=[project.name]), {
            'display_name': 'project 2', # Project 2 already exist
            'name': 'newproject',
            'description': '',
            'access': Project.ACCESS_PUBLIC,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already a project')
        response = self.client.post(reverse('edit-project', args=[project.name]), {
            'display_name': 'New project name',
            'name': 'admin', # reserved name
            'description': '',
            'access': Project.ACCESS_PUBLIC,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'this URL is reserved')
        response = self.client.post(reverse('edit-project', args=[project.name]), {
            'display_name': 'New project name',
            'name': project.name,
            'access': project.access,
        })
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertEqual(project.display_name, 'New project name')

    def test_project_delete(self):
        count = Project.objects.count()
        project = Project.objects.first()
        response = self.client.get(reverse('delete-project', args=[project.name]))
        self.assertEqual(response.status_code, 405) # get method not allowed
        response = self.client.post(reverse('delete-project', args=[project.name]))
        self.assertRedirects(response, reverse('list-project'))
        self.assertEqual(Project.objects.count(), count - 1)

    def test_project_subscribe_unsubscribe(self):
        self.client.logout()
        self.client.login(username='user1', password='user1')
        user = User.objects.get(username='user1')
        project = Project.objects.get(name='project-1')
        self.assertFalse(user in project.subscribers.all())
        response = self.client.get(reverse('unsubscribe-project', args=[project.name]), follow=True)
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        self.assertContains(response, 'not subscribed to this project')
        response = self.client.get(reverse('subscribe-project', args=[project.name]), follow=True)
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        self.assertContains(response, 'must set an email')
        user.email = 'user@example.com'
        user.notifications = User.NOTIFICATIONS_NEVER
        user.save()
        response = self.client.get(reverse('subscribe-project', args=[project.name]), follow=True)
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        self.assertContains(response, 'must enable notifications')
        user.notifications = User.NOTIFICATIONS_OTHERS
        user.save()
        response = self.client.get(reverse('subscribe-project', args=[project.name]))
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertTrue(user in project.subscribers.all())
        response = self.client.get(reverse('subscribe-project', args=[project.name]), follow=True)
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        self.assertContains(response, 'already subscribed')
        response = self.client.get(reverse('unsubscribe-project', args=[project.name]))
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertFalse(user in project.subscribers.all())
        # test redirect with next=
        response = self.client.get(reverse('subscribe-project', args=[project.name])+'?next='+reverse('profile'))
        self.assertRedirects(response, reverse('profile'))
        response = self.client.get(reverse('unsubscribe-project', args=[project.name])+'?next='+reverse('profile'))
        self.assertRedirects(response, reverse('profile'))

    # Issue

    def test_issue_list(self):
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('list-issue', args=[project.name]))
        self.assertEqual(response.status_code, 200)
        url = reverse('list-issue', args=['not-existing-project'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login')+'?next='+url)

    def test_issue_add(self):
        count = Issue.objects.count()
        project = Project.objects.get(name='project-1')
        response = self.client.get(reverse('add-issue', args=[project.name]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add-issue', args=[project.name]), {
            'title': 'new issue',
            'description': 'New issue.',
        })
        issue = Issue.objects.get(title='new issue')
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertEqual(Issue.objects.count(), count + 1)
        response = self.client.post(reverse('add-issue', args=[project.name]), {
            'title': 'new issue bis',
        })
        issue = Issue.objects.get(title='new issue bis')
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertEqual(Issue.objects.count(), count + 2)

    def test_issue_edit(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.first()
        count = issue.events.count()
        response = self.client.get(reverse('edit-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit-issue', args=[project.name, issue.id]), {
            'title': 'new title',
        }, follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'updated successfully')
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.title, 'new title')
        self.assertEqual(issue.events.count(), count + 1)
        response = self.client.post(reverse('edit-issue', args=[project.name, issue.id]), {
            'title': 'new title',
            'description': 'new description',
        }, follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'updated successfully')
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.description, 'new description')
        response = self.client.post(reverse('edit-issue', args=[project.name, issue.id]), {
            'title': 'new title',
            'description': 'new description',
        }, follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'not modified')

    def test_issue_details(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='Issue 1')
        response = self.client.get(reverse('show-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)
        issue = project.issues.get(title='THE Issue 2')
        response = self.client.get(reverse('show-issue', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)

    def test_issue_comment_add(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='Issue 1')
        count = issue.comments.count()
        response = self.client.get(reverse('add-comment', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add-comment', args=[project.name, issue.id]), {
            'comment': 'New comment.',
        })
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.comments.count(), count + 1)

    def test_issue_comment_add_and_close(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='Issue 1')
        comments = issue.comments.count()
        events = issue.events.count()
        response = self.client.get(reverse('add-comment', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add-comment', args=[project.name, issue.id]), {
            'comment': 'New comment.',
            'change-state': '',
        })
        self.assertRedirects(response, reverse('list-issue', args=[project.name]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.comments.count(), comments + 1)
        self.assertEqual(issue.events.count(), events + 2)
        self.assertTrue(issue.closed)

    def test_issue_comment_add_and_reopen(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='Issue 1')
        issue.closed = True
        issue.save()
        comments = issue.comments.count()
        events = issue.events.count()
        response = self.client.get(reverse('add-comment', args=[project.name, issue.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add-comment', args=[project.name, issue.id]), {
            'comment': 'New comment.',
            'change-state': '',
        })
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.comments.count(), comments + 1)
        self.assertEqual(issue.events.count(), events + 2)
        self.assertFalse(issue.closed)

    def test_issue_comment_edit(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='THE Issue 2')
        comment = issue.comments.first()
        response = self.client.get(reverse('edit-comment', args=[project.name, issue.id, comment.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit-comment', args=[project.name, issue.id, comment.id]), {
            'comment': 'New comment.',
        }, follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'modified successfully')
        comment = Event.objects.get(pk=comment.pk)
        self.assertEqual(comment.additionnal_section, 'New comment.')
        response = self.client.post(reverse('edit-comment', args=[project.name, issue.id, comment.id]), {
            'comment': 'New comment.',
        }, follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'not modified')

    def test_issue_comment_delete(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='THE Issue 2')
        count = issue.comments.count()
        comment = issue.comments.first()
        response = self.client.get(reverse('delete-comment', args=[project.name, issue.id, comment.id]))
        self.assertEqual(response.status_code, 405) # get method not allowed
        response = self.client.post(reverse('delete-comment', args=[project.name, issue.id, comment.id]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.comments.count(), count - 1)

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

    def test_issue_add_remove_label(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='Issue 1')
        count = issue.events.count()
        label = project.labels.get(name='documentation')
        self.assertFalse(label in issue.labels.all())
        response = self.client.get(reverse('add-label-to-issue', args=[project.name, issue.id, label.id]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertTrue(label in issue.labels.all())
        self.assertEqual(issue.events.count(), count + 1)
        response = self.client.get(reverse('remove-label-from-issue', args=[project.name, issue.id, label.id]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertFalse(label in issue.labels.all())
        self.assertEqual(issue.events.count(), count + 2)

    def test_issue_add_remove_milestone(self):
        project = Project.objects.get(name='project-1')
        issue = project.issues.get(title='Issue 1')
        count = issue.events.count()
        milestone = project.milestones.get(name='v1.0')
        self.assertEqual(issue.milestone, None)
        response = self.client.get(reverse('add-milestone-to-issue', args=[project.name, issue.id, milestone.name]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.milestone, milestone)
        self.assertEqual(issue.events.count(), count + 1)
        milestone = project.milestones.get(name='v2.0')
        response = self.client.post(reverse('add-milestone', args=[project.name])+'?issue='+str(issue.id), {
            'name': 'new-milestone',
            'color': '#00ff00',
        }, follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        project = Project.objects.get(pk=project.pk)
        milestone = project.milestones.get(name='new-milestone')
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.milestone, milestone)
        self.assertEqual(issue.events.count(), count + 2)
        response = self.client.get(reverse('remove-milestone-from-issue', args=[project.name, issue.id, milestone.name]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertEqual(issue.milestone, None)
        self.assertEqual(issue.events.count(), count + 3)

    def test_issue_subscribe_unsubscribe(self):
        self.client.logout()
        self.client.login(username='user1', password='user1')
        user = User.objects.get(username='user1')
        issue = Issue.objects.get(title='Issue 1')
        project = issue.project
        self.assertFalse(user in issue.subscribers.all())
        response = self.client.get(reverse('unsubscribe-issue', args=[project.name, issue.id]), follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'not subscribed to this issue')
        response = self.client.get(reverse('subscribe-issue', args=[project.name, issue.id]), follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'must set an email')
        user.email = 'user@example.com'
        user.notifications = User.NOTIFICATIONS_NEVER
        user.save()
        response = self.client.get(reverse('subscribe-issue', args=[project.name, issue.id]), follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'must enable notifications')
        user.notifications = User.NOTIFICATIONS_OTHERS
        user.save()
        response = self.client.get(reverse('subscribe-issue', args=[project.name, issue.id]))
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        issue = Issue.objects.get(pk=issue.pk)
        self.assertTrue(user in issue.subscribers.all())
        response = self.client.get(reverse('subscribe-issue', args=[project.name, issue.id]), follow=True)
        self.assertRedirects(response, reverse('show-issue', args=[project.name, issue.id]))
        self.assertContains(response, 'already subscribed to this issue')
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
        count = project.labels.count()
        response = self.client.get(reverse('add-label', args=[project.name]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add-label', args=[project.name]), {
            'name': 'test-label',
            'color': '#ff0000',
        })
        self.assertRedirects(response, reverse('list-label', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertEqual(project.labels.count(), count + 1)

    def test_label_edit(self):
        project = Project.objects.get(name='project-1')
        label = project.labels.first()
        response = self.client.get(reverse('edit-label', args=[project.name, label.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit-label', args=[project.name, label.id]), {
            'name': 'new-label-name',
            'color': label.color,
        })
        self.assertRedirects(response, reverse('list-label', args=[project.name]))
        label = Label.objects.get(pk=label.pk)
        self.assertEqual(label.name, 'new-label-name')

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
        count = project.milestones.count()
        response = self.client.get(reverse('add-milestone', args=[project.name]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add-milestone', args=[project.name]), {
            'name': 'new-version',
        })
        self.assertRedirects(response, reverse('list-milestone', args=[project.name]))
        project = Project.objects.get(pk=project.pk)
        self.assertEqual(project.milestones.count(), count + 1)

    def test_milestone_edit(self):
        project = Project.objects.get(name='project-1')
        milestone = project.milestones.first()
        response = self.client.get(reverse('edit-milestone', args=[project.name, milestone.name]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit-milestone', args=[project.name, milestone.name]), {
            'name': 'new-milestone-name',
        })
        self.assertRedirects(response, reverse('list-milestone', args=[project.name]))
        milestone = Milestone.objects.get(pk=milestone.pk)
        self.assertEqual(milestone.name, 'new-milestone-name')

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
