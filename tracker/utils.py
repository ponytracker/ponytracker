from django.utils.safestring import mark_safe

from markdown import markdown


def markdown_to_html(value):
    # set extensions here if needed
    return mark_safe(markdown(value, safe_mode='escape'))
