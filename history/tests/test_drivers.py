from django.http import response
from django.urls.base import reverse
from django.test import TestCase, client

from history.models import Circuits, Constructors, Drivers, Races


class TestDriversView(TestCase):
    '''
    Testuje widok kierowcow na podstawie bazy zawierajacej informacje z lat 2000-2021(do GP UK)
    '''
    fixtures = ["post2000db.json"]

    def test_simple_view(self):
        '''
        Testuje tylko czy podstrony kierowcow dzialaja
        '''
        vettel = Drivers.objects.get(surname="Vettel")
        alonso = Drivers.objects.get(surname="Alonso")
        leclerc = Drivers.objects.get(surname="Leclerc")

        for driver in [vettel, alonso, leclerc]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["driver"], driver)

    def test_last_race(self):
        '''
        Testuje czy pobieram prawidlowo ostatni wyscig
        '''
        vettel = Drivers.objects.get(surname="Vettel")
        alonso = Drivers.objects.get(surname="Alonso")
        schumacher = Drivers.objects.get(nickname="michael_schumacher")

        vettel_alonso_last_race = Races.objects.get(year=2021,
                                                    circuit__country="UK")
        schumacher_last_race = Races.objects.get(year=2012,
                                                 circuit__country="Brazil")

        for driver, race in [(vettel, vettel_alonso_last_race),
                             (alonso, vettel_alonso_last_race),
                             (schumacher, schumacher_last_race)]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["last_race"], race)

    def test_first_race(self):
        '''
        Sprawdzam czy prawidlowo pobieram pierwszy wyscig
        '''
        vettel = Drivers.objects.get(surname="Vettel")
        alonso = Drivers.objects.get(surname="Alonso")
        leclerc = Drivers.objects.get(surname="Leclerc")

        vettel_first = Races.objects.get(year=2007, circuit__country="USA")
        alonso_first = Races.objects.get(year=2001,
                                         circuit__country="Australia")
        leclerc_first = Races.objects.get(year=2018,
                                          circuit__country="Australia")

        for driver, race in [(vettel, vettel_first), (alonso, alonso_first),
                             (leclerc, leclerc_first)]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["first_race"], race)

    def test_one_race(self):
        '''
        Sprawdzam sytuacje gdy kierowca wystapil tylko w jednym wyscigu F1
        '''
        aitken = Drivers.objects.get(surname="Aitken")
        aitken_race = Races.objects.get(year=2020, round=16)

        response = self.client.get(
            reverse("history:driver_details", args=(aitken.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["first_race"], aitken_race)
        self.assertEqual(response.context["last_race"], aitken_race)

    def test_related_drivers(self):
        '''
        Sprawdzam czy prawidlowo przeszukuje kierowcow o tym samym nazwisku
        '''
        schumachers = Drivers.objects.filter(surname="Schumacher")
        vettel = Drivers.objects.get(surname="Vettel")

        for driver, family in [(vettel, []),
                               (schumachers[0], schumachers[1:])]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertCountEqual(response.context["related_drivers"], family)

    def test_teams(self):
        '''
        Sprawdzam czy prawidłowo wybieram informacje o zespole
        '''
        vettel = Drivers.objects.get(surname="Vettel")

        bmw_sauber = Constructors.objects.get(name="BMW Sauber")
        toro_rosso = Constructors.objects.get(name="Toro Rosso")
        red_bull = Constructors.objects.get(name="Red Bull")
        ferrari = Constructors.objects.get(name="Ferrari")
        aston_martin = Constructors.objects.get(name="Aston Martin")
        vettel_teams = [(2007, [bmw_sauber, toro_rosso]), (2008, [toro_rosso]),
                        (2009, [red_bull]), (2010, [red_bull]),
                        (2011, [red_bull]), (2012, [red_bull]),
                        (2013, [red_bull]), (2014, [red_bull]),
                        (2015, [ferrari]), (2016, [ferrari]),
                        (2017, [ferrari]), (2018, [ferrari]),
                        (2019, [ferrari]), (2020, [ferrari]),
                        (2021, [aston_martin])]

        aitken = Drivers.objects.get(surname="Aitken")
        williams = Constructors.objects.get(name="Williams")
        aitken_teams = [(2020, [williams])]

        for driver, teams in [(vettel, vettel_teams), (aitken, aitken_teams)]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertCountEqual(response.context["teams"], teams)

    def test_wins(self):
        '''
        Sprawdzam czy poprawnie licze liczbe zwyciestw dla danego kierowcy
        '''
        vettel = Drivers.objects.get(surname="Vettel")
        alonso = Drivers.objects.get(surname="Alonso")
        leclerc = Drivers.objects.get(surname="Leclerc")
        aitken = Drivers.objects.get(surname="Aitken")

        vettel_wins = 53
        alonso_wins = 32
        leclerc_wins = 2
        aitken_wins = 0

        for driver, wins in [(vettel, vettel_wins), (alonso, alonso_wins),
                             (leclerc, leclerc_wins), (aitken, aitken_wins)]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["wins"], wins)

    def test_podiums(self):
        '''
        Sprawdzam czy poprawnie obliczam liczbe podiow dla danego kierowcy
        '''
        vettel = Drivers.objects.get(surname="Vettel")
        alonso = Drivers.objects.get(surname="Alonso")
        leclerc = Drivers.objects.get(surname="Leclerc")
        aitken = Drivers.objects.get(surname="Aitken")

        vettel_podiums = 122
        alonso_podiums = 97
        leclerc_podiums = 13
        aitken_podiums = 0

        for driver, podiums in [(vettel, vettel_podiums),
                                (alonso, alonso_podiums),
                                (leclerc, leclerc_podiums),
                                (aitken, aitken_podiums)]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["podiums"], podiums)

    def test_pole_positions(self):
        '''
        Sprawdzam czy poprawnie obliczam liczbe pole position dla danego kierowcy
        '''
        vettel = Drivers.objects.get(surname="Vettel")
        alonso = Drivers.objects.get(surname="Alonso")
        leclerc = Drivers.objects.get(surname="Leclerc")
        aitken = Drivers.objects.get(surname="Aitken")

        vettel_poles = 57
        alonso_poles = 22
        leclerc_poles = 9
        aitken_poles = 0

        for driver, poles in [(vettel, vettel_poles), (alonso, alonso_poles),
                              (leclerc, leclerc_poles),
                              (aitken, aitken_poles)]:
            response = self.client.get(
                reverse("history:driver_details", args=(driver.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["pole_positions"], poles)