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
def first_few(items, arg='item', max_items=5):
    if items.exists():
        if items.count() <= max_items:
            return ', '.join(map(lambda x: x.__str__(), items.all()))
        else:
            r = ', '.join(map(lambda x: x.__str__(),
                items.all()[0:max_items-1]))
            plural = 's' if items.count() > max_items else ''
            r += ', ... (%s other%s)' \
                % (items.count() - max_items + 1, plural)
            return r
    else:
        return 'no ' + arg + 's'
