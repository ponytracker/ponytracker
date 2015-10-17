from __future__ import unicode_literals

from django import template

from tracker.utils import markdown_to_html


register = template.Library()


@register.simple_tag(takes_context=True)
def markdown(context, value, include_domain=False):
    project = context['project']
    return markdown_to_html(value, project)
