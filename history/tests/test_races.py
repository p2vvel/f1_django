from history.models import Qualifying, Races, Results
from django.urls.base import reverse
from django.test import TestCase


class RaceViewTests(TestCase):
    fixtures = ["post2000db.json"]
    def test_simple_view(self):
        '''
        Sprawdzam tylko, czy prawidlowo dziala podstrona wyscigow
        '''
        races = [
            Races.objects.get(year=year, round=round)
            for (year, round) in [(2000, 1), (2005, 5), (2013, 11), (2017, 17), (2020, 15), (2021, 15)]
        ]

    


        for race in []:
            response = self.client.get(
                reverse("history:race_details", args=(race.pk, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["race"], race)

    def test_results(self):
        '''
        Sprawdzam czy prawidlowo pobieram informacje o wynikach wyscigu
        '''
        races_rounds = [(2000, 1), (2005, 5), (2013, 11), (2017, 17), (2020, 15)]

        races = [Races.objects.get(round=round, year=year) for (year, round) in races_rounds]
        races_results = [list(Results.objects.filter(race=race)) for race in races]

        for race, results in zip(races, races_results):
            response = self.client.get(
                reverse("history:race_details", args=(race.pk, )))
            self.assertEqual(response.status_code, 200)
            self.assertCountEqual(response.context["results"], results)

    def test_qualifying(self):
        '''
        Sprawdzam czy prawidlowo pobieram informacje o wynikach kwalifikacji
        '''
        races_rounds = [(2000, 1), (2005, 5), (2013, 11), (2017, 17), (2020, 15)]

        races = [Races.objects.get(round=round, year=year) for (year, round) in races_rounds]
        qualifying_results = [list(Qualifying.objects.filter(race=race)) for race in races]

        for race, quali in zip(races, qualifying_results):
            response = self.client.get(
                reverse("history:race_details", args=(race.pk, )))
            self.assertEqual(response.status_code, 200)
            self.assertCountEqual(response.context["qualifying"], quali)