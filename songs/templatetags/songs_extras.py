from django import template

register = template.Library()


@register.filter
def make_title(s):
    s = [x.title() for x in s.split('_')]
    return ' '.join(s)
