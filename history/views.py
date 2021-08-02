from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import context
from django.urls.base import reverse


# Create your views here.
from django.views import generic
from .models import Circuits, Constructors, Drivers, Races, Results


def group_elements(data, index_key=lambda x: x[0], value_key=lambda x: x[1]):
    indexes = set([index_key(k) for k in data])
    result = {k: [] for k in indexes}
    for k in data:
        result[index_key(k)].append(value_key(k))
    return list(result.items())


class DriverView(generic.DetailView):
    model = Drivers
    context_object_name = "driver"
    template_name = "driver.html"
    slug_url_kwarg = "nick"  # nazwa zmiennej w urlconf (plik url.py)
    slug_field = "nickname"  # nazwa pola w modelu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # dont have to write context["driver"] all time, stores chosen driver data
        my_driver = context["driver"]

        # pobieram informacje o pierwszym wyscigu danego kierowcy
        try:
            context["first_race"] = (
                Results.objects.filter(driver=my_driver)
                .order_by("race__year", "race__round")[0]
                .race
            )
        except Exception as e:
            context["first_race"] = None

        # pobieram informacje o ostatnim (dotychczas) wyscigu danego kierowcy
        try:

            context["last_race"] = (
                Results.objects.filter(driver=my_driver)
                .order_by("-race__year", "-race__round")[0]
                .race
            )
        except Exception as e:
            context["last_race"] = None

        # fetch informations about drivers with same surname (e.g. Schumachers or Verstappens)
        try:
            context["related_drivers"] = Drivers.objects.filter(
                surname=my_driver.surname
            ).exclude(pk=my_driver.id)
        except Exception as e:
            context["related_drivers"] = []

        # fetching teams data
        try:
            # pobieram wszystkie informacje o rezultatach, gdzie jest jest moje id, wybieram z nich informacje o konstruktorze i roku
            temp = (
                Results.objects.filter(driver=my_driver)
                .values("race__year", "constructor")
                .distinct()
            )

            for k in temp:
                k["constructor"] = Constructors.objects.get(pk=k["constructor"])
            temp = group_elements(
                temp,
                index_key=lambda x: x["race__year"],
                value_key=lambda x: x["constructor"],
            )
            temp.sort(key=lambda x: x[0], reverse=True)
            context["teams"] = temp
        except Exception as e:
            context["teams"] = None

        return context


class ConstructorView(generic.DetailView):
    model = Constructors
    context_object_name = "constructor"
    template_name = "constructor.html"
    slug_field = "nickname"
    slug_url_kwarg = "nick"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_constructor = context["constructor"]
        try:
            temp = (
                Results.objects.filter(constructor=my_constructor)
                .values("driver", "race__year")
                .distinct()
            )
            for k in temp:
                k["driver"] = Drivers.objects.get(pk=k["driver"])
            temp = group_elements(
                temp,
                index_key=lambda x: x["race__year"],
                value_key=lambda x: x["driver"],
            )
            temp.sort(key=lambda x: x[0], reverse=True)
            context["drivers"] = temp
        except Exception as e:
            context["drivers"] = []

        return context


class CircuitView(generic.DetailView):
    model = Circuits
    context_object_name = "circuit"
    template_name = "circuit.html"
    slug_field = "nickname"
    slug_url_kwarg = "nick"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_circuit = context["circuit"]
        try:
            pass
            temp = Races.objects.filter(circuit=my_circuit)
            temp = group_elements(
                temp, index_key=lambda x: x.year, value_key=lambda x: x
            )
            temp.sort(reverse=True)
            context["races"] = temp
        except Exception as e:
            context["races"]

        return context


class RaceView(generic.DetailView):
    model = Races
    context_object_name = "race"
    template_name="race.html"