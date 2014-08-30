from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def boolean(value):
    if value:
        glyph = 'ok'
    else:
        glyph = 'remove'
    return mark_safe('<span class="glyphicon glyphicon-'
            + glyph + '" style="vertical-align: middle;"></span>')
