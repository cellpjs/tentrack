from django import template

register = template.Library()

@register.filter
def halfminus(value):
    return -(value/2)
