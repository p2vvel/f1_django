from history.models import Circuits, Races
from django.urls.base import reverse
from django.test import TestCase

from history.utils import group_elements


class CircuitViewTests(TestCase):
    #obraz bazy po GP UK, przed GP Wegier
    fixtures = ["post2000db.json"]

    def test_view(self):
        '''
        Sprawdzam tylko czy prawidłowo dziala ladowanie widoku
    n   '''
        circuits = [
            Circuits.objects.get(name__contains=k)
            for k in ("Monza", "Silverstone", "Spa")
        ]

        for circuit in circuits:
            response = self.client.get(
                reverse("history:circuit_details", args=(circuit.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["circuit"], circuit)

    def test_races(self):
        '''
        Sprawdam czy prawidłowo pobieram wyscigi
        '''
        silverstone = Circuits.objects.get(name__contains="Silverstone")
        #yapf: disable
        silverstone_races = group_elements(list(zip(list(range(2000, 2021)) + [2020, 2021],
            list(Races.objects.filter(name__contains="British",year__lte=2020).order_by("year")) +
            list(Races.objects.filter(name__contains="70")) +
            list(Races.objects.filter(name__contains="British", year=2021).order_by("year")))))
        #yapf: enable

        monza = Circuits.objects.get(name__contains="Monza")
        monza_races = group_elements(
            list(
                zip(
                    range(2000, 2021),
                    Races.objects.filter(
                        name__contains="Italian").order_by("year"))))

        zandvoort = Circuits.objects.get(name__contains="Zandvoort")
        #wyscig jeszcze sie nei odbyl w momencie pobierania stanu testowej bazy danych
        zandvoort_races = []

        self.maxDiff = None

        for circuit, races in [(silverstone, silverstone_races),
                               (monza, monza_races),
                               (zandvoort, zandvoort_races)]:
            response = self.client.get(
                reverse("history:circuit_details", args=(circuit.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertCountEqual(response.context["races"], races)