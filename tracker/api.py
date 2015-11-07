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
from sys import version_info as python_version


@csrf_exempt
@require_http_methods(["POST"])
def email_recv(request):

    if not hasattr(settings, 'REPLY_EMAIL') \
            or not hasattr(settings, 'EMAIL_KEY'):
        return HttpResponse(status=501) # Not Implemented

    key = request.POST.get('key')
    if key != settings.EMAIL_KEY:
        raise PermissionDenied

    if 'email' not in request.FILES:
        raise HttpResponse(status=400) # Bad Request

    msg = request.FILES['email']
    msg = email.message_from_file(msg)

    mfrom = msg.get('From')
    mto = msg.get('To')
    subject = msg.get('Subject')

    if msg.is_multipart():
        msgs = msg.get_payload()
        for m in msgs:
            if m.get_content_type == 'text/plain':
                content = m.get_payload(decode=True)
                break
        else:
            content = msgs[0].get_payload(decode=True)
    else:
        content = msg.get_payload(decode=True)

    if python_version < (3,):
        content = content.decode('utf-8')

    addr = settings.REPLY_EMAIL
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

    return HttpResponse()
