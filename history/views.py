from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import context


# Create your views here.
from django.views import generic
from .models import Drivers, Races

class DriverView(generic.DetailView):
    model = Drivers
    context_object_name = "driver"
    template_name = "driver.html"
    slug_url_kwarg = "nick" #nazwa zmiennej w urlconf (plik url.py)
    slug_field = "nickname" #nazwa pola w modelu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["driver"]["last_race"]
        #TODO: dodaj informacje o pierwszym i ostatnim wyscigu danego kierowcy!!!
        try:
            #pobieram informacje o pierwszym i ostatnim (dotychczas wyscigu danego kierowcy)
            temp = Races.objects.filter(driver=context["driver"]).order_by("date")
            last_race, first_race = temp[-1], temp[0]
            context["driver"].last_race = last_race
            context["driver"].first_race = first_race
        except:
            pass
            
        return context