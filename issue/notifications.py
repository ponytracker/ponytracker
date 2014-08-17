from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings

from issue.models import *


def notify_new_issue(issue):

    project = issue.project

    dests = project.subscribers.all().distinct()

    if hasattr(settings, 'FROM_ADDR'):
        from_addr = settings.FROM_ADDR
    else:
        return

    subject = "[PonyTracker] New issue: %s (%s)" %(issue.title, project.name)

    data = []

    for dest in dests:

        if dest == issue.author:
            continue

        dest_addr = dest.email
        if not dest_addr:
            continue

        c = {
            'dest': dest.username,
            'author': issue.author.username,
            'title': issue.title,
            'description:': issue.description,
            'uri': settings.BASE_URL \
                + reverse('show-issue', args=[project.name, issue.id]),
        }

        message = render_to_string('emails/new_issue.html', c)

        data += [(subject, message, from_addr, [dest_addr])]

    send_mass_mail(tuple(data))


def notify_new_comment(event):

    issue = event.issue
    project = issue.project

    dests = issue.subscribers.all()
    dests |= project.subscribers.all()
    dests = dests.distinct()

    if hasattr(settings, 'FROM_ADDR'):
        from_addr = settings.FROM_ADDR
    else:
        return

    subject = "[PonyTracker] New comment - %s (%s)" %(issue.title, project.name)

    data = []

    for dest in dests:

        if dest == event.author:
            continue

        dest_addr = dest.email
        if not dest_addr:
            continue

        c = {
            'dest': dest.username,
            'author': event.author.username,
            'title': issue.title,
            'comment': event.additionnal_section,
            'uri': settings.BASE_URL \
                + reverse('show-issue', args=[project.name, issue.id]),
        }

        message = render_to_string('emails/new_comment.html', c)

        data += [(subject, message, from_addr, [dest_addr])]

    send_mass_mail(tuple(data))
