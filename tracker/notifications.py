from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings

if 'djcelery' in settings.INSTALLED_APPS:
    from tracker.tasks import send_mass_mail
else:
    from django.core.mail import send_mass_mail

from accounts.models import User


__all__ = [
    'notify_new_issue', 'notify_new_comment',
    'notify_close_issue', 'notify_reopen_issue'
]


def notify_new_issue(issue):

    project = issue.project
    dests = project.subscribers.all().distinct()

    subject = "[%s] %s" % (project, issue.title)
    sender = issue.author

    data = {
        'description': issue.description,
        'uri': settings.BASE_URL + reverse('show-issue',
            args=[project.name, issue.id]),
    }

    notify_by_email(data, 'new_issue', subject, sender, dests)

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

    subject = "Re: [%s] %s" % (project, issue.title)
    sender = event.author

    data = {
        'comment': event.additionnal_section,
        'uri': settings.BASE_URL + reverse('show-issue',
            args=[project.name, issue.id]),
    }

    notify_by_email(data, template, subject, sender, dests)


def notify_by_email(data, template, subject, sender, dests):

    message = render_to_string('emails/%s.html' % template, data)

    if hasattr(settings, 'FROM_ADDR'):
        from_addr = settings.FROM_ADDR
    else:
        return

    from_addr = '%s <%s>' % (sender.fullname or sender.username, from_addr)

    mails = []

    for dest in dests:

        if dest.notifications == User.NOTIFICATIONS_NEVER:
            continue
        if dest == sender \
                and dest.notifications == User.NOTIFICATIONS_OTHERS:
            continue
        dest_addr = dest.email
        if not dest_addr:
            continue

        mails += [(subject, message, from_addr, [dest_addr])]

    if 'djcelery' in settings.INSTALLED_APPS:
        send_mass_mail.delay(tuple(mails))
    else:
        send_mass_mail(tuple(mails))
