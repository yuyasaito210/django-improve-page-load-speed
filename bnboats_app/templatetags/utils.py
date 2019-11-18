from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def replace_space(value):
    return value.replace(" ", "_")