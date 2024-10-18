from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return round(float(value) * float(arg), 2)
    except (ValueError, TypeError):
        return ''
