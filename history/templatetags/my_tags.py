from django import template

register = template.Library()

from history.utils import get_country_code
from django.utils.safestring import mark_safe


#value is race results data
@register.filter  #have to register custom template to make it work
def any_laptime(value):
    '''Custom template tag created to check if there's any fastest laptime info in race results data'''
    return any([k.fastest_laptime for k in value])


@register.filter
def all_q(value):
    '''Custom template tag created to check if there's any q1, q2 or q3 laptime info in qualifying results data'''
    return any([k.q1 for k in value]) and any([k.q2 for k in value]) and any(
        [k.q3 for k in value])


@register.filter
def only_q1(value):
    '''Custom template tag created to check if there's any q1, q2 or q3 laptime info in qualifying results data'''
    return any([k.q1 for k in value
                ]) and not any([k.q2 for k in value] + [k.q3 for k in value])


def get_country_flag_url(country_name):
    return "https://www.countryflags.io/{country}/{type}/{size}.png".format(
        country=get_country_code(country_name), type="flat", size="32")

@register.filter(is_safe=True)
def country_flag_image(value):
    url = get_country_flag_url(value)

    return mark_safe(
        "<img src=%s alt=%s>" %
        (url,
         value))  #musze uzyc tej instrukcji zeby pozwolilo mi zwrocic html
