from .utils import *
from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase, client
from datetime import datetime

class RaceViewTests(TestCase):
    def test_race_view(self):
        circuit = create_circuit(name="Monza", nickname="monza")
        race = create_race(circuit=circuit, name="Race of nothing", date=datetime.now())

        response = self.client.get(reverse("history:race_details", args=(race.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_results_data(self):
        circuit = create_circuit("Monza")
        race = create_race(
            circuit=circuit,
            name="Italian Grand Prix",
            date=datetime.now(),
            year=2013,
            round=7,
        )
        status = create_status("Finished")

        ferrari = create_constructor(name="Ferrari", nickname="ferrari")
        red_bull = create_constructor(name="Red Bull", nickname="red_bull")

        vettel = create_driver(name="Sebastian", surname="Vettel", nickname="vettel")
        webber = create_driver(name="Mark", surname="Webber", nickname="webber")
        alonso = create_driver(name="Fernando", surname="Alonso", nickname="alonso")
        massa = create_driver(name="Felipe", surname="Massa", nickname="massa")

        result1 = create_result(
            race=race,
            driver=vettel,
            constructor=red_bull,
            status=status,
            grid=1,
            position=1,
            position_info=1,
            position_order=1,
            points=25,
        )
        result2 = create_result(
            race=race,
            driver=alonso,
            constructor=ferrari,
            status=status,
            grid=2,
            position=2,
            position_info=2,
            position_order=2,
            points=18,
        )
        result3 = create_result(
            race=race,
            driver=webber,
            constructor=red_bull,
            status=status,
            grid=3,
            position=3,
            position_info=3,
            position_order=3,
            points=15,
        )
        result4 = create_result(
            race=race,
            driver=massa,
            constructor=ferrari,
            status=status,
            grid=4,
            position=4,
            position_info=4,
            position_order=4,
            points=12,
        )

        race2 = create_race(
            circuit=circuit,
            name="Italian Grand Prix2",
            date=datetime.now(),
            year=2014,
            round=7,
        )
        result10 = create_result(
            race=race2,
            driver=vettel,
            constructor=red_bull,
            status=status,
            grid=1,
            position=1,
            position_info=1,
            position_order=1,
            points=25,
        )
        result20 = create_result(
            race=race2,
            driver=webber,
            constructor=red_bull,
            status=status,
            grid=2,
            position=2,
            position_info=2,
            position_order=2,
            points=18,
        )
        result30 = create_result(
            race=race2,
            driver=alonso,
            constructor=ferrari,
            status=status,
            grid=3,
            position=3,
            position_info=3,
            position_order=3,
            points=15,
        )

        response = self.client.get(reverse("history:race_details", args=(race.pk,)))
        self.assertEqual(
            list(response.context["results"]), [result1, result2, result3, result4]
        )

    def test_qualifying_data(self):
        circuit = create_circuit("Monza")
        race = create_race(
            circuit=circuit,
            name="Italian Grand Prix",
            date=datetime.now(),
            year=2013,
            round=7,
        )

        ferrari = create_constructor(name="Ferrari", nickname="ferrari")
        red_bull = create_constructor(name="Red Bull", nickname="red_bull")

        vettel = create_driver(name="Sebastian", surname="Vettel", nickname="vettel")
        webber = create_driver(name="Mark", surname="Webber", nickname="webber")
        alonso = create_driver(name="Fernando", surname="Alonso", nickname="alonso")
        massa = create_driver(name="Felipe", surname="Massa", nickname="massa")

        quali1 = create_qualifying(
            race=race, driver=vettel, constructor=red_bull, position=1, number=5
        )
        quali2 = create_qualifying(
            race=race, driver=alonso, constructor=ferrari, position=2, number=5
        )
        quali3 = create_qualifying(
            race=race, driver=webber, constructor=red_bull, position=3, number=5
        )
        quali4 = create_qualifying(
            race=race, driver=massa, constructor=ferrari, position=4, number=5
        )

        response = self.client.get(reverse("history:race_details", args=(race.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["qualifying"]), [quali1, quali2, quali3, quali4]
        )
