# '2018/8/15 20:04'
# coding=utf-8


import random
from django import template
register = template.Library()


@register.filter
def che(value):
    return random.choice(value)
