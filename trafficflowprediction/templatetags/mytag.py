from django import template

register = template.Library()


@register.filter
def label_class(value, cls):
    return value.label_tag(attrs={'class': cls})
