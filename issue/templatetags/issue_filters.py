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

@register.filter
def first_few(items, arg='item'):
    if items.exists():
        if items.count() < 4:
            return ', '.join(map(lambda x: x.__str__(), items.all()))
        else:
            r = ', '.join(map(lambda x: x.__str__(), items.all()[0:3]))
            plural = 's' if items.count() > 4 else ''
            r += ', ... (%s other%s)' % (items.count() - 3, plural)
            return r
    else:
        return 'no ' + arg + 's'
