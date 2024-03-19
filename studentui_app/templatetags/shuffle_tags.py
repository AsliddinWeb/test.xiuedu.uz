from django import template
import random

register = template.Library()

@register.filter
def shuffle_answers(value):
    return sorted(value, key=lambda x: random.random())