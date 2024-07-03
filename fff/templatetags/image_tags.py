#Djordje Loncar 2021/0076
import base64
from django import template

register = template.Library()


@register.filter
def to_base64(binary_data):
    if binary_data:
        return base64.b64encode(binary_data).decode('utf-8')
    return ''
