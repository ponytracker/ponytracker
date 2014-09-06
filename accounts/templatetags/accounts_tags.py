from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape


register = template.Library()


@register.inclusion_tag('accounts/tags/delete_modal.html')
def delete_modal():
    return {}

@register.inclusion_tag('accounts/tags/delete_modal_js.html')
def delete_modal_js():
    return {}
