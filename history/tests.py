from datetime import date, datetime, timedelta
import unittest
from unittest import result
from django.db.models import constraints
from django.test import TestCase, client
from django.test.testcases import TransactionTestCase
from django.urls.base import reverse
from django.utils import timezone


# Create your tests here.

from .models import Drivers, Circuits, Races, Results, Status, Constructors, Seasons
from .views import group_elements

# TODO: models objects generators (driver, constructor, circuit)


def create_driver(name, surname, nickname="test_driver", code="TST", number=12, url=""):
    url = nickname if url == "" else url
    return Drivers.objects.create(
        name=name,
        surname=surname,
        nickname=nickname,
        code=code,
        number=number,
        wiki_url=url,
    )


def create_circuit(name, nickname="nickname", url=""):
    url = name.lower() + "_" + nickname if url == "" else url
    return Circuits.objects.create(name=name, nickname=nickname, wiki_url=url)


def create_constructor(name, nickname="test_constructor", url=""):
    url = name.lower() + "_" + nickname if url == "" else url
    return Constructors.objects.create(name=name, nickname=nickname, wiki_url=url)


def create_race(circuit, name, date, year=2013, round=7):
    return Races.objects.create(
        circuit=circuit, date=date, name=name, year=year, round=round
    )


def create_result(
    race, driver, constructor, status, grid=1, position_order=2, points=10, laps=50
):
    return Results.objects.create(
        race=race,
        driver=driver,
        constructor=constructor,
        grid=grid,
        position_order=position_order,
        points=points,
        laps=laps,
        status=status,
    )


def create_status(status_info):
    return Status.objects.create(status_info=status_info)


class TestGrouping(TestCase):
    """tests for function grouping elements, useful for e.g. showing drivers in seasons in chosen team"""

    def test_grouping_elements(self):
        data = [(2000, 12), (2000, 20), (2000, 2), (2001, 202), (2001, 33), (2004, 0)]
        expected_result = [(2000, [12, 20, 2]), (2001, [202, 33]), (2004, [0])]
        self.assertCountEqual(group_elements(data), expected_result)

    def test_different_keys(self):
        data = [
            ("ferrari", 2001),
            ("red bull", 2002),
            ("aston martin", 2002),
            ("ferrari", 2004),
        ]
        expected_results = [
            (2001, ["ferrari"]),
            (2002, ["red bull", "aston martin"]),
            (2004, ["ferrari"]),
        ]

        expected_results2 = [
            ("ferrari", [2001, 2004]),
            ("red bull", [2002]),
            ("aston martin", [2002]),
        ]

        self.assertCountEqual(
            group_elements(data, index_key=lambda x: x[1], value_key=lambda x: x[0]),
            expected_results,
        )
        self.assertCountEqual(
            group_elements(data, index_key=lambda x: x[0], value_key=lambda x: x[1]),
            expected_results2,
        )


class StrModelsTests(TestCase):
    def test_drivers_str(self):
        """
        Tests for Drivers model __str__
        """
        # test for driver with code and number
        driver_code = Drivers(
            number=12,
            code="COD",
            name="Forename",
            surname="Surname",
            nickname="driverref",
        )
        self.assertEqual(str(driver_code), "[COD 12]Forename Surname")
        # test for driver number only
        driver_no_code = Drivers(
            number=12, name="Forename", surname="Surname", nickname="driverref"
        )
        self.assertEqual(str(driver_no_code), "[12]Forename Surname")
        # test for driver with code only
        driver_code = Drivers(
            code="COD", name="Forename", surname="Surname", nickname="driverref"
        )
        self.assertEqual(str(driver_code), "[COD]Forename Surname")
        # test for driver with nothing
        driver_no_code = Drivers(
            name="Forename", surname="Surname", nickname="driverref"
        )
        self.assertEqual(str(driver_no_code), "Forename Surname")

    def test_circuit_str(self):
        """
        Tests for Circuits model __str__
        """
        circuit = Circuits(name="Test Circuit")
        self.assertEqual(str(circuit), "Test Circuit")

    def test_constructor_str(self):
        """
        Tests for Constructors model __str__
        """
        constructor = Constructors(name="Test constructor", nickname="constructorref")
        self.assertEqual(str(constructor), "Test constructor")

    def test_race_str(self):
        """
        Tests for Races model __str__
        """
        circuit = create_circuit(name="Monza")
        race = Races(year=2013, round=2, name="Test race", circuit=circuit)
        self.assertEqual(str(race), "Test race")


class DriverViewTests(TestCase):
    def test_driver_view_slug(self):
        """
        tests if driver details view works correctly when using slug identifier in urlconf
        """
        driver = Drivers.objects.create(
            name="Forename", surname="Surname", nickname="driverref"
        )
        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname,))
        )
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

        results1 = create_result(
            race=race1, driver=driver, constructor=constructor, status=status
        )
        results2 = create_result(
            race=race2, driver=driver, constructor=constructor, status=status
        )
        results3 = create_result(
            race=race3, driver=driver, constructor=constructor, status=status
        )
        results4 = create_result(
            race=race4, driver=driver, constructor=constructor, status=status
        )

        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname,))
        )
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
            reverse("history:driver_details", args=(driver.nickname,))
        )
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
        results = create_result(
            race=race, driver=driver, constructor=constructor, status=status
        )

        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname,))
        )
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
        driver3 = create_driver(name="Johnny", surname="Doe", nickname="johnnydoe")

        driver4 = create_driver(name="Ed", surname="Ed", nickname="ed")
        driver5 = create_driver(name="Edd", surname="Edd", nickname="edd")
        driver6 = create_driver(name="Eddy", surname="Eddy", nickname="eddy")

        response = self.client.get(
            reverse("history:driver_details", args=(driver1.nickname,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["related_drivers"], [driver2, driver3])

    def test_driver_teams(self):
        """
        Tests for checking if function finding drivers team is ok
        """
        driver = create_driver(name="John", surname="Doe", nickname="johnnydoodoo")
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
        results1 = create_result(
            race=race1, driver=driver, constructor=ferrari, status=status
        )
        results2 = create_result(
            race=race2, driver=driver, constructor=red_bull, status=status
        )
        results3 = create_result(
            race=race3, driver=driver, constructor=red_bull, status=status
        )
        results4 = create_result(
            race=race4, driver=driver, constructor=red_bull, status=status
        )
        results5 = create_result(
            race=race5, driver=driver, constructor=aston_martin, status=status
        )
        results5 = create_result(
            race=race6, driver=driver, constructor=ferrari, status=status
        )
        results5 = create_result(
            race=race7, driver=driver, constructor=aston_martin, status=status
        )

        # second driver for better testing
        driver2 = create_driver(name="Gregor", surname="Florida", nickname="jersey")
        results11 = create_result(
            race=race1, driver=driver2, constructor=aston_martin, status=status
        )
        results22 = create_result(
            race=race2, driver=driver2, constructor=ferrari, status=status
        )
        results33 = create_result(
            race=race3, driver=driver2, constructor=red_bull, status=status
        )

        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname,))
        )
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


class CircuitViewTests(TestCase):
    def test_view(self):
        circuit = create_circuit(name="Monza", nickname="monza")
        response = self.client.get(
            reverse("history:circuit_details", args=(circuit.nickname,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["circuit"], circuit)

    def test_races_list(self):
        circuit = create_circuit(name="Monza", nickname="monza")
        circuit2 = create_circuit(name="Silverstone", nickname="silverstone")

        race1 = create_race(circuit=circuit, name="Race1", date = datetime.now(), round=2, year = 2012)
        race2 = create_race(circuit=circuit, name="Race2", date = datetime.now(), round=2, year = 2013)
        race3 = create_race(circuit=circuit2, name="Race3", date = datetime.now(), round=2, year = 2014)
        race4 = create_race(circuit=circuit, name="Race4", date = datetime.now(), round=2, year = 2015)
        race5 = create_race(circuit=circuit, name="Race5", date = datetime.now(), round=3, year = 2015)

        response = self.client.get(reverse("history:circuit_details", args=(circuit.nickname,)))
        self.assertEqual(response.status_code, 200)

        expected_result = [
            (2012, [race1]),
            (2013, [race2]),
            (2015, [race4, race5])
        ]

        self.assertCountEqual(response.context["races"], expected_result)