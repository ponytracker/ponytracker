from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings

if 'djcelery' in settings.INSTALLED_APPS:
    from tracker.tasks import send_mass_mail
else:
    from django.core.mail import send_mass_mail


__all__ = [
    'notify_new_issue', 'notify_new_comment',
    'notify_close_issue', 'notify_reopen_issue'
]


def notify_new_issue(issue):

    project = issue.project
    dests = project.subscribers.all().distinct()

    if hasattr(settings, 'FROM_ADDR'):
        from_addr = settings.FROM_ADDR
    else:
        return

    subject = "[%s] %s" % (project, issue.title)

    data = []
    for dest in dests:

        if dest == issue.author:
            continue

        dest_addr = dest.email
        if not dest_addr:
            continue

        c = {
            'description': issue.description,
            'uri': settings.BASE_URL + reverse('show-issue',
                args=[project.name, issue.id]),
        }

        message = render_to_string('emails/new_issue.html', c)

        data += [(subject, message,
            "%s <%s>" % (issue.author.username, from_addr), [dest_addr])]

    if 'djcelery' in settings.INSTALLED_APPS:
        send_mass_mail.delay(tuple(data))
    else:
        send_mass_mail(tuple(data))


def notify_new_comment(event):
    notify_event(event, 'new_comment')


def notify_close_issue(event):
    notify_event(event, 'close_issue')


def notify_reopen_issue(event):
    notify_event(event, 'reopen_issue')


def notify_event(event, template):

    issue = event.issue
    project = issue.project

    dests = issue.subscribers.all()
    dests |= project.subscribers.all()
    dests = dests.distinct()

    if hasattr(settings, 'FROM_ADDR'):
        from_addr = settings.FROM_ADDR
    else:
        return

    subject = "Re: [%s] %s" % (project, issue.title)

    data = []

    for dest in dests:

        if dest == event.author:
            continue

        dest_addr = dest.email
        if not dest_addr:
            continue

        c = {
            'comment': event.additionnal_section,
            'uri': settings.BASE_URL + reverse('show-issue',
                args=[project.name, issue.id]),
        }

        message = render_to_string('emails/%s.html' % template, c)

        data += [(subject, message,
            '%s <%s>' % (event.author.username, from_addr), [dest_addr])]

    if 'djcelery' in settings.INSTALLED_APPS:
        send_mass_mail.delay(tuple(data))
    else:
        send_mass_mail(tuple(data))
