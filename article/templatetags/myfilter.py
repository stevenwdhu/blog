from django import template
from django.utils.http import urlencode
from django.utils import timezone

register = template.Library()


@register.filter
def dictpop(value: dict, arg=None):
    if arg:
        try:
            output = value.copy()
            output.pop(arg)
            return output
        except KeyError:
            return value
    else:
        return value


@register.filter
def urlstr(value: dict):
    if isinstance(value, dict):
        return urlencode(value)
    else:
        raise TypeError
    
# @register.filter
# def time_since(value):
#     now = timezone.now()
#     diff = now - value
#
#     if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
#         return 'Now'
#
#     if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
#         return f"{diff.seconds // 60} min"
#
#     if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
#         return str(math.floor(diff.seconds / 3600)) + "小时前"
#
#     if diff.days >= 1 and diff.days < 30:
#         return str(diff.days) + "天前"
#
#     if diff.days >= 30 and diff.days < 365:
#         return str(math.floor(diff.days / 30)) + "个月前"
#
#     if diff.days >= 365:
#         return str(math.floor(diff.days / 365)) + "年前"
