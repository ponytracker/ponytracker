from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from accounts.models import User
from tracker.utils import hexdigest_sha256
from tracker.models import *
from tracker.notifications import notify_new_comment

import email
import re


@csrf_exempt
@require_http_methods(["POST"])
def email_recv(request):

    key = request.POST.get('key')
    if key != settings.EMAIL_KEY:
        raise PermissionDenied

    msg = request.POST.get('email')
    msg = email.message_from_string(msg)

    mfrom = msg.get('From')
    mto = msg.get('To')
    subject = msg.get('Subject')
    content = msg.get_payload()
    if msg.is_multipart():
        content = content[0].get_payload(decode=True)

    addr = getattr(settings, 'REPLY_ADDR', settings.FROM_ADDR)
    pos = addr.find('@')
    name = addr[:pos]
    domain = addr[pos:]

    p = re.compile('^%s\+(?P<project>[-\w]+)\.issue-(?P<issue>[0-9]+)(\.(?P<event>[0-9]+))?\.(?P<user>[0-9]+)\.(?P<token>[a-z0-9]+)%s$' % (name, domain))
    m = p.match(mto)
    if not m:
        raise Http404

    project = get_object_or_404(Project, name=m.group('project'))
    issue = get_object_or_404(Issue, project=project, id=m.group('issue'))
    event = m.group('event')
    if event:
        event = get_object_or_404(Event, issue=issue, pk=event)
    user = get_object_or_404(User, pk=m.group('user'))
    token = m.group('token')

    mid = '%s.issue-%d' % (project.name, issue.id)
    if event:
        mid += '.%s' % event.pk
    reference_token = hexdigest_sha256(settings.SECRET_KEY, mid, user.pk)

    if token != reference_token:
        raise PermissionDenied

    event = Event(issue=issue, author=user, code=Event.COMMENT,
                  additionnal_section=content)
    event.save()
    issue.subscribers.add(user)
    notify_new_comment(event)
    issue.save()

    return HttpResponse('')
