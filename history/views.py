from datetime import datetime
from history.forms import SearchForm
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse

# Create your views here.
from django.views import generic
from django.views.generic.detail import DetailView
from .models import Circuits, Constructors, Constructorstandings, Drivers, Driverstandings, Qualifying, Races, Results, Seasons

from .utils import group_elements, fill_empty_races

from django.db.models import Min, Q, Value
from django.views.generic.list import ListView
from django.db.models.functions import Substr

from django.db.models.functions import Concat


def index(request):
    current_year = datetime.now().year
    #jesli sezon sie jeszcze nie zaczal, bede wyswietlac informacje o starym sezonie
    if Seasons.count_races(year=current_year) == 0:
        current_year -= 1

    return redirect(reverse("history:season_details", args=(current_year, )))


class DriverView(generic.DetailView):
    model = Drivers
    context_object_name = "driver"
    template_name = "driver.html"
    slug_url_kwarg = "nick"  # nazwa zmiennej w urlconf (plik url.py)
    slug_field = "nickname"  # nazwa pola w modelu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_driver = context["driver"]

        # pobieram informacje o pierwszym wyscigu danego kierowcy
        try:
            context["first_race"] = (Results.objects.filter(
                driver=my_driver).order_by("race__year",
                                           "race__round")[0].race)
        except Exception as e:
            context["first_race"] = None

        # pobieram informacje o ostatnim (dotychczas) wyscigu danego kierowcy
        try:

            context["last_race"] = (Results.objects.filter(
                driver=my_driver).order_by("-race__year",
                                           "-race__round")[0].race)
        except Exception as e:
            context["last_race"] = None

        # fetch informations about drivers with same surname (e.g. Schumachers or Verstappens)
        try:
            context["related_drivers"] = Drivers.objects.filter(
                surname=my_driver.surname).exclude(pk=my_driver.id)
        except Exception as e:
            context["related_drivers"] = []

        # fetching teams data
        try:
            # pobieram wszystkie informacje o rezultatach, gdzie jest jest moje id, wybieram z nich informacje o konstruktorze i roku
            temp = (Results.objects.filter(driver=my_driver).values(
                "race__year", "constructor").distinct())

            for k in temp:
                k["constructor"] = Constructors.objects.get(
                    pk=k["constructor"])
            temp = group_elements(
                temp,
                index_key=lambda x: x["race__year"],
                value_key=lambda x: x["constructor"],
            )
            temp.sort(key=lambda x: x[0], reverse=True)
            context["teams"] = temp
        except Exception as e:
            context["teams"] = None


        #informacje o podiach
        try:
            temp = Results.objects.filter(
                Q(driver=my_driver)
                & (Q(position=1) | Q(position=2) | Q(position=3))).count()
            context["podiums"] = temp
        except Exception as e:
            context["podiums"] = None

        #liczba wyscigow
        try:
            context["races_count"] = Results.objects.filter(
                driver=my_driver).count()
        except:
            context["races_count"] = None

        #najwyzsza pozycja startowa i jej wystapienia dla danego kierowcy
        try:
            #0 oznacza start z pit boxow, dlatego musze to wziac pod uwage przy wyszukiwaniu najnizszej pozycji startowej
            highest_grid = Results.objects.filter(driver=my_driver,
                                                  grid__gt=0).aggregate(
                                                      Min("grid"))["grid__min"]
            grid_count = Results.objects.filter(driver=my_driver,
                                                grid=highest_grid).count()
            context["highest_grid"] = {
                "grid": highest_grid,
                "count": grid_count
            }
        except:
            context["highest_grid"] = None

        #najlepsze miejsce w wyscigu i jego wystapienia dla danego kierowcy
        try:
            highest_position = Results.objects.filter(
                driver=my_driver).aggregate(Min("position"))["position__min"]
            position_count = Results.objects.filter(
                driver=my_driver, position=highest_position).count()
            context["highest_position"] = {
                "position": highest_position,
                "count": position_count
            }
        except:
            context["highest_position"] = None

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
            temp = Results.objects\
                .filter(constructor=my_constructor)\
                .values("driver", "race__year")\
                .distinct()

            for k in temp:
                k["driver"] = Drivers.objects.get(pk=k["driver"])

            temp = group_elements(temp,
                                  index_key=lambda x: x["race__year"],
                                  value_key=lambda x: x["driver"])
            temp.sort(key=lambda x: x[0], reverse=True)
            context["drivers"] = temp
        except Exception as e:
            context["drivers"] = []

        #liczba wyscigow
        try:
            context["races_count"] = Results.objects.filter(
                constructor=my_constructor).values("race").distinct().count()
        except:
            context["races_count"] = None

        #najwyzsza pozycja startowa i jej wystapienia
        try:
            grid = Results.objects.filter(constructor=my_constructor,
                                          grid__gt=0).aggregate(
                                              Min("grid"))["grid__min"]
            count = Results.objects.filter(constructor=my_constructor,
                                           grid=grid).count()
            context["highest_grid"] = {"grid": grid, "count": count}
        except:
            context["highest_grid"] = None

        #najwyzsza pozycja zajeta w wyscigu i jej wystapienia
        try:
            position = Results.objects.filter(
                constructor=my_constructor).aggregate(
                    Min("position"))["position__min"]
            count = Results.objects.filter(constructor=my_constructor,
                                           position=position).count()
            context["highest_position"] = {
                "position": position,
                "count": count
            }
        except:
            context["highest_position"] = None

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
            temp = Races.objects.filter(circuit=my_circuit,
                                        results__isnull=False).distinct()
            temp = group_elements(temp,
                                  index_key=lambda x: x.year,
                                  value_key=lambda x: x)
            temp.sort(reverse=True)
            context["races"] = temp
        except Exception as e:
            context["races"]

        return context


class RaceView(generic.DetailView):
    model = Races
    context_object_name = "race"
    template_name = "race.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_race = context["race"]

        #informacje o wynikach wyscigu
        try:
            temp = Results.objects\
                .filter(race=my_race)\
                .order_by("position_order")

            context["results"] = temp
        except Exception as e:
            context["results"] = []

        # informacje o kwalifikacjach
        try:
            temp = Qualifying.objects\
                .filter(race=my_race)\
                .order_by("position")

            context["qualifying"] = temp
        except Exception as e:
            context["qualifying"] = []

        return context


class SeasonView(DetailView):
    model = Seasons
    template_name = "seasons.html"
    context_object_name = "season"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_season = context["season"]

        #liczba wyscigow(dotychczasowych i calkowita) i o zakonczeniu sezonu
        try:
            context["finished"] = Seasons.season_finished(my_season.year)
            context["total_races"] = Seasons.count_total_races(my_season.year)
            context["organized_races"] = Seasons.count_races(my_season.year)
        except Exception as e:
            context["finished"] = None
            context["total_races"] = None
            context["organized_races"] = None

        #informacje o nastepym sezonie
        try:
            context["next_season"] = Seasons.objects.get(year=my_season.year +
                                                         1)
        except:
            context["next_season"] = None

        #informacje o poprzednim sezonie
        try:
            context["previous_season"] = Seasons.objects.get(
                year=my_season.year - 1)
        except:
            context["previous_season"] = None

        #informacje o miejscach w stawce sa grupowane wg ostatniego odbytego wyscigu
        if (last_race := Seasons.get_latest_race(year=my_season.year)):
            #kierowcy
            try:
                temp = Driverstandings.objects\
                        .filter(race=last_race)\
                        .order_by("position")

                context["drivers"] = temp
            except Exception as e:
                context["drivers"] = []
            #konstruktorzy
            try:
                temp = Constructorstandings.objects\
                    .filter(race=last_race)\
                    .order_by("position")
                context["constructors"] = temp
            except Exception as e:
                context["constructors"] = []
        else:
            context["drivers"] = []
            context["constructors"] = []

        #wyscigi
        try:
            context["races"] = Races.objects.filter(
                year=my_season.year).order_by("round")
        except:
            context["races"] = None

        if context["drivers"] and context["organized_races"]:
            try:
                temp = []
                for driver in [k.driver for k in context["drivers"]]:
                    temp.append([
                        driver,
                        Results.objects.filter(
                            race__year=my_season.year,
                            driver=driver).order_by("race__round")
                    ])

                for index, races in enumerate(temp):
                    temp[index][1] = fill_empty_races(
                        races[1], context["organized_races"])

                # context["drivers_classification"] = map(
                #     lambda x: fill_empty_races(x[1], context["organized_races"]
                #                                ), temp)
                context["drivers_classification"] = temp
            except:
                context["drivers_classification"] = None

        return context


class SeasonsListView(ListView):
    model = Seasons
    context_object_name = "seasons"
    template_name = "seasons_list.html"
    ordering = "-year"
    paginate_by = 10


class AlphabeticalSearchListView(ListView):
    '''Klasa bazowa, zeby nie pisac dwa razy tego samego kodu dla widokow list kierowcow, torow i konstruktorow'''
    paginate_by = 20

    def get_queryset(self):
        letter = self.request.GET.get("letter")
        search_query = self.request.GET.get("search_query")

        if search_query:
            return self.get_queryset_search(
                search_query)  #przypadek kiedy user wpisal tekst do wyszukania
        elif letter:
            return self.get_queryset_alphabetical(
                letter)  #przypadek kiedy mam litere alfabetu
        else:
            return self.get_queryset_regular()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["letter"] = self.request.GET.get("letter")
        context["search_query"] = self.request.GET.get("search_query")

        context["available_letters"] = self.get_queryset_letters()
        context["form"] = SearchForm(self.request.GET)
        return context


class DriversListView(AlphabeticalSearchListView):
    template_name = "drivers_list.html"

    def get_queryset_alphabetical(self, letter):
        '''Zwraca nazwiska kierowcow, ktorych nazwiska zaczynaja sie na podana litere'''
        try:
            return Drivers.objects.filter(
                surname__istartswith=letter).order_by("surname", "name")
        except:
            return None

    def get_queryset_regular(self):
        '''Zwraca kierowcow ktorzy startuja w aktualnym sezonie'''
        try:
            return Drivers.objects.filter(
                results__race__year=Seasons.get_current_season()).distinct(
                ).order_by("surname", "name")
        except Exception as e:
            return None

    def get_queryset_letters(self):
        try:
            return sorted([
                k.lower() for k in Drivers.objects.all().values_list(
                    Substr("surname", 1, 1), flat=True).distinct()
            ])
        except:
            return None

    def get_queryset_search(self, search_query):
        try:
            return Drivers.objects.annotate(
                fullname=Concat("name", Value(" "), "surname")).filter(
                    fullname__icontains=search_query)
        except Exception as e:
            print("ERROR: %s" % e)
            return None


class ConstructorsListView(AlphabeticalSearchListView):
    template_name = "constructors_list.html"

    def get_queryset_alphabetical(self, letter):
        '''Zwraca nazwy konstruktorow, ktorych nazwy zaczynaja sie na podana litere'''
        try:
            return Constructors.objects.filter(
                name__istartswith=letter).order_by("name")
        except:
            return None

    def get_queryset_regular(self):
        '''Zwraca konstruktorow, ktorzy startuja w aktualnym sezonie'''
        try:
            return Constructors.objects.filter(
                results__race__year=Seasons.get_current_season()).distinct(
                ).order_by("name")
        except Exception as e:
            return None

    def get_queryset_letters(self):
        try:
            return sorted([
                k.lower() for k in Constructors.objects.all().values_list(
                    Substr("name", 1, 1), flat=True).distinct()
            ])
        except:
            return None

    def get_queryset_search(self, search_query):
        try:
            return Constructors.objects.filter(name__icontains=search_query)
        except:
            return None


class CircuitsListView(AlphabeticalSearchListView):
    template_name = "circuits_list.html"

    def get_queryset_alphabetical(self, letter):
        '''Zwraca tory, ktorych nazwy zaczynaja sie na podana litere'''
        try:
            return Circuits.objects.filter(
                name__istartswith=letter).order_by("name")
        except:
            return None

    def get_queryset_regular(self):
        '''Zwraca tory, na ktorych odbywaja sie w wyscigi w aktualnym sezonie'''
        try:
            return Circuits.objects.filter(
                races__year=Seasons.get_current_season()).distinct().order_by(
                    "name")
        except:
            return None

    def get_queryset_letters(self):
        '''Zwraca pierwsze litery nazw torow'''
        try:
            return sorted([
                k.lower() for k in Circuits.objects.all().values_list(
                    Substr("name", 1, 1), flat=True).distinct()
            ])
        except:
            return None

    def get_queryset_search(self, search_query):
        try:
            return Circuits.objects.filter(name__icontains=search_query)
        except:
            return None