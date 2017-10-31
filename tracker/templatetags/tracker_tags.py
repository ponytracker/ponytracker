from __future__ import unicode_literals

from django import template
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
    project = context['project']
    return author.url(project.name)

@register.simple_tag(takes_context=True)
def can_edit(context, event):
    request = context['request']
    return event.editable_by(request)

@register.filter
def get_item(dic, valeur):
    return dic.get(valeur, None)
