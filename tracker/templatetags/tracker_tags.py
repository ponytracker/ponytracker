from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape


register = template.Library()


@register.inclusion_tag('tracker/tags/user_badge.html')
def user_badge(user):
    return {'user': user}


@register.simple_tag
def label_style(label):

    if label.inverted:
        fg = '#fff'
    else:
        fg = '#000'

    style = "background-color: {bg}; color: {fg}; vertical-align: middle;"

    return style.format(bg=label.color, fg=fg)


@register.simple_tag
def labeled(label):

    html = '<span class="label" style="{style}">{name}</span>'

    return mark_safe(html.format(style=label_style(label),
        name=escape(label.name)))


@register.simple_tag
def same_label(label):

    url = reverse('list-issue', kwargs={'project': label.project.name})
    url += '?q=is:open%20label:' + label.quotted_name

    return mark_safe(url)


@register.simple_tag
def same_milestone(milestone):

    url = reverse('list-issue', kwargs={'project': milestone.project.name})
    url += '?q=is:open%20milestone:' + milestone.name

    return mark_safe(url)


@register.simple_tag(takes_context=True)
def same_author(context, author):

    url = reverse('list-issue', kwargs={'project': context['project'].name})
    url += '?q=is:open%20author:' + author.username

    return mark_safe(url)
