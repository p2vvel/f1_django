from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import context


# Create your views here.
from django.views import generic
from .models import Drivers, Races, Results


class DriverView(generic.DetailView):
    model = Drivers
    context_object_name = "driver"
    template_name = "driver.html"
    slug_url_kwarg = "nick"  # nazwa zmiennej w urlconf (plik url.py)
    slug_field = "nickname"  # nazwa pola w modelu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # print("Driver: {}".format(context["driver"]))\
        # pobieram informacje o pierwszym wyscigu danego kierowcy
        try:
            context["first_race"] = Results.objects.filter(driver=context["driver"]).order_by("race__year", "race__round")[0].race
        except Exception as e:
            context["first_race"] = None

        # pobieram informacje o ostatnim (dotychczas) wyscigu danego kierowcy
        try:
             
            context["last_race"] = Results.objects.filter(driver=context["driver"]).order_by("-race__year", "-race__round")[0].race
        except Exception as e:
            context["last_race"] = None

        #fetch informations about drivers with same surname (e.g. Schumachers or Verstappens)
        try:
            context["related_drivers"] = Drivers.objects.filter(surname=context["driver"].surname).exclude(pk=context["driver"].id)
        except Exception as e:
            print("ERROR: %s" % e)
            context["related_drivers"] = []

        return context
