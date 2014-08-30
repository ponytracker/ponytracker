from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.inclusion_tag('permissions/tags/perm_form.html', takes_context=True)
def add_perm_form(context):
    return {
        'form': context['add_form'],
        'type': 'add',
        'title': 'Add permission',
        'action': reverse('add-global-permission'),
    }


@register.inclusion_tag('permissions/tags/perm_form.html', takes_context=True)
def edit_perm_form(context):
    return {
        'form': context['edit_form'],
        'type': 'edit',
        'title': 'Edit permission',
    }
