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

@register.filter
def smart_time(value):
    now = timezone.now()
    diff = now - value

    days = diff.days

    if days == 0:
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            return f"{hours} saat öncə"
        elif minutes > 0:
            return f"{minutes} dəq öncə"
        else:
            return "indi"
    elif days == 1:
        return "Dünən"
    else:
        return f"{days} gün öncə"