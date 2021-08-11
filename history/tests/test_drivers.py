from datetime import datetime, timedelta

from django.shortcuts import redirect
from .utils import *
from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase, client


class DriverViewTests(TestCase):
    def test_driver_view_slug(self):
        """
        tests if driver details view works correctly when using slug identifier in urlconf
        """
        driver = Drivers.objects.create(name="Forename",
                                        surname="Surname",
                                        nickname="driverref")
        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], driver)

    def test_first_last_race(self):
        """
        Tests for checking drivers last and first race if there are some races in db
        """
        driver = create_driver(name="John", surname="Doe")
        constructor = create_constructor(name="Race Team")
        circuit = create_circuit(name="Monza")
        status = create_status(status_info="Nothing xd")
        race1 = create_race(
            circuit=circuit,
            name="Race of Nothing #1",
            year=2011,
            round=3,
            date=timezone.now(),
        )
        race2 = create_race(
            circuit=circuit,
            name="Race of Nothing #2",
            year=2013,
            round=5,
            date=timezone.now(),
        )
        race3 = create_race(
            circuit=circuit,
            name="Race of Nothing #3",
            year=2020,
            round=10,
            date=timezone.now(),
        )
        race4 = create_race(
            circuit=circuit,
            name="Race of Nothing #4",
            year=2021,
            round=5,
            date=timezone.now(),
        )

        results1 = create_result(race=race1,
                                 driver=driver,
                                 constructor=constructor,
                                 status=status)
        results2 = create_result(race=race2,
                                 driver=driver,
                                 constructor=constructor,
                                 status=status)
        results3 = create_result(race=race3,
                                 driver=driver,
                                 constructor=constructor,
                                 status=status)
        results4 = create_result(race=race4,
                                 driver=driver,
                                 constructor=constructor,
                                 status=status)

        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname, )))
        self.assertEqual(response.status_code, 200)
        # checks first race
        self.assertEqual(response.context["first_race"], race1)
        # checks last_race
        self.assertEqual(response.context["last_race"], race4)

    def test_first_last_race_empty_races(self):
        """
        Tests for checking drivers last and first race if there are no races in db for this driver
        """
        driver = create_driver(name="John", surname="Doe")
        constructor = create_constructor(name="Race Team")
        circuit = create_circuit(name="Monza")
        status = create_status(status_info="Nothing xd")

        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["first_race"], None)
        self.assertEqual(response.context["last_race"], None)

    def test_first_last_race_one_race(self):
        """
        Tests for checking drivers last and first race if there are some races in db
        """
        driver = create_driver(name="John", surname="Doe")
        constructor = create_constructor(name="Race Team")
        circuit = create_circuit(name="Monza")
        status = create_status(status_info="Nothing xd")
        race = create_race(
            circuit=circuit,
            name="Race of Nothing #1",
            year=2011,
            round=3,
            date=timezone.now(),
        )
        results = create_result(race=race,
                                driver=driver,
                                constructor=constructor,
                                status=status)

        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname, )))
        self.assertEqual(response.status_code, 200)
        # checks first race
        self.assertEqual(response.context["first_race"], race)
        # checks last_race
        self.assertEqual(response.context["last_race"], race)

    def test_related_drivers(self):
        """
        Tests for finding drivers with the same surname
        """
        driver1 = create_driver(name="John", surname="Doe", nickname="johndoe")
        driver2 = create_driver(name="Joe", surname="Doe", nickname="joedoe")
        driver3 = create_driver(name="Johnny",
                                surname="Doe",
                                nickname="johnnydoe")

        driver4 = create_driver(name="Ed", surname="Ed", nickname="ed")
        driver5 = create_driver(name="Edd", surname="Edd", nickname="edd")
        driver6 = create_driver(name="Eddy", surname="Eddy", nickname="eddy")

        response = self.client.get(
            reverse("history:driver_details", args=(driver1.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["related_drivers"],
                              [driver2, driver3])

    def test_driver_teams(self):
        """
        Tests for checking if function finding drivers team is ok
        """
        driver = create_driver(name="John",
                               surname="Doe",
                               nickname="johnnydoodoo")
        ferrari = create_constructor(name="Ferrari")
        red_bull = create_constructor(name="Red Bull")
        aston_martin = create_constructor(name="Aston Martin")
        circuit1 = create_circuit(name="Monza")
        circuit2 = create_circuit(name="Nurburgring")
        status = create_status(status_info="Default status")
        race1 = create_race(
            circuit=circuit1,
            name="Race of Nothing 1",
            year=2011,
            round=3,
            date=timezone.now(),
        )
        race2 = create_race(
            circuit=circuit2,
            name="Race of Nothing 2",
            year=2013,
            round=2,
            date=timezone.now(),
        )
        race3 = create_race(
            circuit=circuit1,
            name="Race of Nothing 3",
            year=2014,
            round=3,
            date=timezone.now(),
        )
        race4 = create_race(
            circuit=circuit1,
            name="Race of Nothing 4",
            year=2015,
            round=5,
            date=timezone.now(),
        )
        race5 = create_race(
            circuit=circuit1,
            name="Race of Nothing 5",
            year=2016,
            round=12,
            date=timezone.now(),
        )
        race6 = create_race(
            circuit=circuit2,
            name="Race of Nothing 6",
            year=2016,
            round=13,
            date=timezone.now(),
        )
        race7 = create_race(
            circuit=circuit2,
            name="Race of Nothing 7",
            year=2017,
            round=11,
            date=timezone.now(),
        )
        results1 = create_result(race=race1,
                                 driver=driver,
                                 constructor=ferrari,
                                 status=status)
        results2 = create_result(race=race2,
                                 driver=driver,
                                 constructor=red_bull,
                                 status=status)
        results3 = create_result(race=race3,
                                 driver=driver,
                                 constructor=red_bull,
                                 status=status)
        results4 = create_result(race=race4,
                                 driver=driver,
                                 constructor=red_bull,
                                 status=status)
        results5 = create_result(race=race5,
                                 driver=driver,
                                 constructor=aston_martin,
                                 status=status)
        results5 = create_result(race=race6,
                                 driver=driver,
                                 constructor=ferrari,
                                 status=status)
        results5 = create_result(race=race7,
                                 driver=driver,
                                 constructor=aston_martin,
                                 status=status)

        # second driver for better testing
        driver2 = create_driver(name="Gregor",
                                surname="Florida",
                                nickname="jersey")
        results11 = create_result(race=race1,
                                  driver=driver2,
                                  constructor=aston_martin,
                                  status=status)
        results22 = create_result(race=race2,
                                  driver=driver2,
                                  constructor=ferrari,
                                  status=status)
        results33 = create_result(race=race3,
                                  driver=driver2,
                                  constructor=red_bull,
                                  status=status)

        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.maxDiff = None

        expected_results = [
            (2011, [ferrari]),
            (2013, [red_bull]),
            (2014, [red_bull]),
            (2015, [red_bull]),
            (2016, [aston_martin, ferrari]),
            (2017, [aston_martin]),
        ]

        self.assertCountEqual(response.context["teams"], expected_results)

    # def test_wins(self):
    #     vettel = create_driver(name="Sebastian",
    #                            surname="Vettel",
    #                            nickname="vettel")
    #     redbull = create_constructor(name="Red Bull", nickname="redbull")
    #     status=create_status(status_info="Finished")
    #     monza = create_circuit(name="Monza", nickanme="monza")
    #     races = [
    #         create_race(circuit=monza,
    #                     name="Race%s" % k,
    #                     date=datetime.now() - timedelta(days=30 * k),
    #                     year=2000 + k,
    #                     round=k) for k in [10, 11, 12, 15, 16, 17, 20]]
    #     results = create_result(
    #         race=races[k], driver=vettel, constructor=redbull, status=status, grid=2, position=1
    #     )