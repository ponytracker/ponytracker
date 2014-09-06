from django import template

from tracker.utils import markdown_to_html


register = template.Library()


@register.filter
def markdown(value):
    return markdown_to_html(value)
