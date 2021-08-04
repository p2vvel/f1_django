
from django import template

register = template.Library()

#value is race results data
@register.filter    #have to register custom template to make it work
def any_laptime(value):
    '''Custom template tag created to check if there's any fastest laptime info in race results data'''
    return any([k.fastest_laptime for k in value])

@register.filter
def all_q(value):
    '''Custom template tag created to check if there's any q1, q2 or q3 laptime info in qualifying results data'''
    return any([k.q1 for k in value]) and any([k.q2 for k in value]) and any([k.q3 for k in value])

@register.filter
def only_q1(value):
    '''Custom template tag created to check if there's any q1, q2 or q3 laptime info in qualifying results data'''
    return any([k.q1 for k in value]) and not any([k.q2 for k in value] + [k.q3 for k in value])