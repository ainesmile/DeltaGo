from django import template
from django.utils import timezone


register = template.Library()


def padding_date(value):
    value = int(value)
    if value < 10:
        return '0' + str(value)
    else:
        return str(value)

def postfix_date(data):
    str = ''
    for item, postfix in data:
        str_item = padding_date(item) + postfix
        str += str_item
    return str

@register.filter(name='human_time_date', expects_localtime=True)
def human_time_date(value):
    data = [
        (value.year, '-'),
        (value.month, '-'),
        (value.day, '')
    ]
    return postfix_date(data)

@register.filter(name='human_time_hour', expects_localtime=True)
def human_time_hour(value):
    data = [
        (value.hour, ':'),
        (value.minute, ':'),
        (value.second, '')
    ]
    return postfix_date(data)