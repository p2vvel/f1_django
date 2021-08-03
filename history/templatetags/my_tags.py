
from django import template

register = template.Library()

#value is race results data
@register.filter    #have to register custom template to make it work
def any_laptime(value):
    '''Custom template tag created to check if there's any fastest laptime info in race results data'''
    return any([k.fastest_laptime for k in value])