from datetime import date, datetime, timedelta
import unittest
from unittest import result
from django.db.models import constraints
from django.test import TestCase, client
from django.test.testcases import TransactionTestCase
from django.urls.base import reverse
from django.utils import timezone

# importing all create_* functions
from .utils import *
from history.utils import group_elements


class TestGrouping(TestCase):
    """tests for function grouping elements, useful for e.g. showing drivers in seasons in chosen team"""
    def test_grouping_elements(self):
        data = [(2000, 12), (2000, 20), (2000, 2), (2001, 202), (2001, 33),
                (2004, 0)]
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
            group_elements(data,
                           index_key=lambda x: x[1],
                           value_key=lambda x: x[0]),
            expected_results,
        )
        self.assertCountEqual(
            group_elements(data,
                           index_key=lambda x: x[0],
                           value_key=lambda x: x[1]),
            expected_results2,
        )


class StrModelsTests(TestCase):
    def test_drivers_str(self):
        """
        Tests for Drivers model __str__
        """
        driver_nothing = Drivers(name="Forename",
                                 surname="Surname",
                                 nickname="driverref")
        self.assertEqual(str(driver_nothing), "Forename Surname")

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
        constructor = Constructors(name="Test constructor",
                                   nickname="constructorref")
        self.assertEqual(str(constructor), "Test constructor")

    def test_race_str(self):
        """
        Tests for Races model __str__
        """
        circuit = create_circuit(name="Monza")
        race = Races(year=2013, round=2, name="Test race", circuit=circuit)
        self.assertEqual(str(race), "Test race")

    def test_result_str(self):
        driver = create_driver(name="Sebastian",
                               surname="Vettel",
                               nickname="vettel")
        circuit = create_circuit(name="Monza", nickname="monza")
        constructor = create_constructor(name="Ferrari", nickname="ferrari")
        race = create_race(
            circuit=circuit,
            name="Italian Grand Prix",
            date=timezone.now(),
            year=2018,
            round=10,
        )
        status = create_status(status_info="Dominated whole race!")
        result = create_result(
            race=race,
            driver=driver,
            constructor=constructor,
            status=status,
            grid=1,
            position=1,
            position_info=1,
            position_order=1,
            points=25,
            laps=62,
        )

        self.assertEqual("2018 Italian Grand Prix, Sebastian Vettel, 1",
                         str(result))

    def test_status_str(self):
        status = create_status(status_info="Nothing special")
        self.assertEqual("Nothing special", str(status))
