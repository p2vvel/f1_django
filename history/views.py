from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import context


# Create your views here.
from django.views import generic
from .models import Constructors, Drivers, Races, Results


class DriverView(generic.DetailView):
    model = Drivers
    context_object_name = "driver"
    template_name = "driver.html"
    slug_url_kwarg = "nick"  # nazwa zmiennej w urlconf (plik url.py)
    slug_field = "nickname"  # nazwa pola w modelu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_driver = context["driver"]   #dont have to write context["driver"] all time, stores chosen driver data
        
        # pobieram informacje o pierwszym wyscigu danego kierowcy
        try:
            context["first_race"] = Results.objects.filter(driver=my_driver).order_by("race__year", "race__round")[0].race
        except Exception as e:
            context["first_race"] = None

        # pobieram informacje o ostatnim (dotychczas) wyscigu danego kierowcy
        try:
             
            context["last_race"] = Results.objects.filter(driver=my_driver).order_by("-race__year", "-race__round")[0].race
        except Exception as e:
            context["last_race"] = None

        #fetch informations about drivers with same surname (e.g. Schumachers or Verstappens)
        try:
            context["related_drivers"] = Drivers.objects.filter(surname=my_driver.surname).exclude(pk=my_driver.id)
        except Exception as e:
            print("ERROR: %s" % e)
            context["related_drivers"] = []

        #fetching teams data
        try:
            #pobieram wszystkie informacje o rezultatach, gdzie jest jest moje id, wybieram z nich informacje o konstruktorze i roku
            temp = [(k.constructor, k.race.year) for k in Results.objects.filter(driver = my_driver)]
            temp = list(set(temp))  #unikalne pary (konstruktor, rok)
            temp.sort(key=lambda x: x[1])
            temp = [ {"year": k[1], "team": k[0]} for k in temp]
            context["teams"] = temp
        except Exception as e:
            print("ERROR: %s" % e)
            context["teams"] = None

        return context
