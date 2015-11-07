from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape


register = template.Library()


@register.inclusion_tag('tracker/tags/user_badge.html')
def user_badge(user):
    return {'user': user}


@register.simple_tag
def labeled(label):

    html = '<span class="label" style="{style}">{name}</span>'

    return mark_safe(html.format(style=label.style, name=escape(label.name)))


@register.simple_tag(takes_context=True)
def same_author(context, author):

    url = reverse('list-issue', kwargs={'project': context['project'].name})
    url += '?q=is:open%20author:' + author.username

    return mark_safe(url)
