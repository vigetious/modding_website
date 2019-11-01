from django import template

register = template.Library()

@register.filter(name="tagSearch")
def tagSearch(tag, term):
    names = tag.names
    for tags in names:
        if tags == term:
            return tags
