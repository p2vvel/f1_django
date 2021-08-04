from .utils import *
from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase, client
from datetime import datetime

class ConstructorViewTests(TestCase):
    def test_constructor_site(self):
        constructor = create_constructor(name="Red Bull", nickname="redbullo")

        response = self.client.get(
            reverse("history:constructor_details", args=(constructor.nickname,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["constructor"], constructor)

    def test_drivers_data(self):
        """tests if site shows correct drivers for each seasons in chosen team"""
        constructor = create_constructor(name="Ferrari", nickname="ferraro")
        driver1 = create_driver(
            name="Michael", surname="Schumacher", nickname="schumacher"
        )
        driver2 = create_driver(name="Fernando", surname="Alonso", nickname="nando")
        driver3 = create_driver(name="Kimi", surname="Raikonnen", nickname="iceman")
        driver4 = create_driver(name="Sebastian", surname="Vettel", nickname="vet")
        driver5 = create_driver(name="Charles", surname="Leclerc", nickname="lec")

        circuit = create_circuit(name="Monza")
        status = create_status(status_info="Nothing to see")

        race1 = create_race(
            circuit=circuit, name="Monza1", date=datetime.now(), year=2008, round=7
        )
        race2 = create_race(
            circuit=circuit, name="Monza2", date=datetime.now(), year=2009, round=3
        )
        race3 = create_race(
            circuit=circuit, name="Monza3", date=datetime.now(), year=2010, round=4
        )
        race4 = create_race(
            circuit=circuit, name="Monza4", date=datetime.now(), year=2011, round=5
        )

        result1 = create_result(
            race=race1, constructor=constructor, status=status, driver=driver1
        )
        result2 = create_result(
            race=race1, constructor=constructor, status=status, driver=driver2
        )

        result3 = create_result(
            race=race2, constructor=constructor, status=status, driver=driver1
        )
        result4 = create_result(
            race=race2, constructor=constructor, status=status, driver=driver2
        )

        result5 = create_result(
            race=race3, constructor=constructor, status=status, driver=driver2
        )
        result6 = create_result(
            race=race3, constructor=constructor, status=status, driver=driver3
        )

        result7 = create_result(
            race=race4, constructor=constructor, status=status, driver=driver3
        )
        result8 = create_result(
            race=race4, constructor=constructor, status=status, driver=driver4
        )
        result9 = create_result(
            race=race4, constructor=constructor, status=status, driver=driver5
        )

        expected_result = [
            (2008, [driver1, driver2]),
            (2009, [driver1, driver2]),
            (2010, [driver2, driver3]),
            (2011, [driver3, driver4, driver5]),
        ]

        response = self.client.get(
            reverse("history:constructor_details", args=(constructor.nickname,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["drivers"], expected_result)
