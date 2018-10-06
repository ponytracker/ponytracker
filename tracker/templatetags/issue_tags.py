from __future__ import unicode_literals

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def issue_url(context, **kwargs):

    manager = context['manager']
    url = reverse('list-issue', kwargs={'project': context['project'].name})
    get_parameters = manager.get_parameters(**kwargs)
    if get_parameters:
        url += '?' + get_parameters

    return mark_safe(url)
