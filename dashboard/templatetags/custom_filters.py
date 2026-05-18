from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def smart_date(value):
    now = timezone.now()
    diff = now - value

    days = diff.days

    if days == 0:
        return "Bu gün"
    elif days == 1:
        return "Dünən"
    else:
        return f"{days} gün əvvəl"