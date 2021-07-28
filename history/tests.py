from datetime import date, datetime, timedelta
import unittest
from django.db.models import constraints
from django.test import TestCase
from django.test.testcases import TransactionTestCase
from django.urls.base import reverse
from django.utils import timezone


# Create your tests here.

from .models import Drivers, Circuits, Races, Results, Status, Constructors, Seasons

# TODO: models objects generators (driver, constructor, circuit)


def create_driver(name, surname, nickname="test_driver", code="TST", number=12, url=''):
    url = nickname if url=='' else url
    return Drivers.objects.create(name=name, surname=surname, nickname=nickname, code=code, number=number, wiki_url=url)


def create_circuit(name, nickname="test_circuit"):
    return Circuits.objects.create(name=name, nickname=nickname)


def create_constructor(name, nickname="test_constructor"):
    return Constructors.objects.create(name=name, nickname=nickname)


def create_race(circuit, name, date, year=2013, round=7):
    return Races.objects.create(circuit=circuit, date=date, name=name, year=year, round=round)


def create_result(race, driver, constructor, status, grid=1, position_order=2, points=10, laps=50):
    return Results.objects.create(race=race, driver=driver, constructor=constructor, grid=grid, position_order=position_order, points=points, laps=laps, status=status)


def create_status(status_info):
    return Status.objects.create(status_info=status_info)

class StrModelsTests(TestCase):
    def test_drivers_str(self):
        '''
        Tests for Drivers model __str__
        '''
        # test for driver with code and number
        driver_code = Drivers(
            number=12, code="COD", name="Forename", surname="Surname", nickname="driverref")
        self.assertEqual(str(driver_code), '[COD 12]Forename Surname')
        # test for driver number only
        driver_no_code = Drivers(
            number=12, name="Forename", surname="Surname", nickname="driverref")
        self.assertEqual(str(driver_no_code), '[12]Forename Surname')
        # test for driver with code only
        driver_code = Drivers(code="COD", name="Forename",
                              surname="Surname", nickname="driverref")
        self.assertEqual(str(driver_code), '[COD]Forename Surname')
        # test for driver with nothing
        driver_no_code = Drivers(
            name="Forename", surname="Surname", nickname="driverref")
        self.assertEqual(str(driver_no_code), 'Forename Surname')

    def test_circuit_str(self):
        '''
        Tests for Circuits model __str__
        '''
        circuit = Circuits(name="Test Circuit")
        self.assertEqual(str(circuit), "Test Circuit")

    def test_constructor_str(self):
        '''
        Tests for Constructors model __str__
        '''
        constructor = Constructors(
            name="Test constructor", nickname="constructorref")
        self.assertEqual(str(constructor), "Test constructor")

    def test_race_str(self):
        '''
        Tests for Races model __str__
        '''
        circuit = create_circuit(name="Monza")
        race_no_circuit = Races(
            year=2013, round=2, name="Test race", circuit=circuit)
        self.assertEqual(str(race_no_circuit), "2#2013 Monza")


class DriverViewTests(TestCase):
    def test_driver_view_slug(self):
        '''
        tests if driver details view works correctly when using slug identifier in urlconf
        '''
        driver = Drivers.objects.create(
            name="Forename", surname="Surname", nickname="driverref")
        response = self.client.get(
            reverse("history:driver_details", args=(driver.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['driver'], driver)

    def test_first_last_race(self):
        '''
        Tests for checking drivers last and first race if there are some races in db
        '''
        driver = create_driver(name="John", surname="Doe")
        constructor = create_constructor(name="Race Team")
        circuit = create_circuit(name="Monza")
        status=create_status(status_info="Nothing xd")
        race1 = create_race(circuit=circuit, name="Race of Nothing #1", year=2011, round=3, date=timezone.now())
        race2 = create_race(circuit=circuit, name="Race of Nothing #2", year=2013, round=5, date=timezone.now())
        race3 = create_race(circuit=circuit, name="Race of Nothing #3", year=2020, round=10, date=timezone.now())
        race4 = create_race(circuit=circuit, name="Race of Nothing #4", year=2021, round=5, date=timezone.now())
        
        results1 = create_result(race=race1, driver=driver, constructor=constructor, status=status)
        results2 = create_result(race=race2, driver=driver, constructor=constructor, status=status)
        results3 = create_result(race=race3, driver=driver, constructor=constructor, status=status)
        results4 = create_result(race=race4, driver=driver, constructor=constructor, status=status)
        
        response = self.client.get(reverse("history:driver_details", args=(driver.nickname,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["first_race"], race1) #checks first race
        self.assertEqual(response.context["last_race"], race4)  #checks last_race

    def test_first_last_race_empty_races(self):
        '''
        Tests for checking drivers last and first race if there are no races in db for this driver
        '''
        driver = create_driver(name="John", surname="Doe")
        constructor = create_constructor(name="Race Team")
        circuit = create_circuit(name="Monza")
        status=create_status(status_info="Nothing xd")

        response = self.client.get(reverse("history:driver_details", args=(driver.nickname,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["first_race"], None)
        self.assertEqual(response.context["last_race"], None)
    
    def test_first_last_race_one_race(self):
        '''
        Tests for checking drivers last and first race if there are some races in db
        '''
        driver = create_driver(name="John", surname="Doe")
        constructor = create_constructor(name="Race Team")
        circuit = create_circuit(name="Monza")
        status=create_status(status_info="Nothing xd")
        race = create_race(circuit=circuit, name="Race of Nothing #1", year=2011, round=3, date=timezone.now())
        results = create_result(race=race, driver=driver, constructor=constructor, status=status)
        
        response = self.client.get(reverse("history:driver_details", args=(driver.nickname,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["first_race"], race) #checks first race
        self.assertEqual(response.context["last_race"], race)  #checks last_race

    def test_related_drivers(self):
        '''
        Tests for finding drivers with the same surname
        '''
        driver1=create_driver(name="John", surname="Doe", nickname="johndoe")
        driver2=create_driver(name="Joe", surname="Doe", nickname="joedoe")
        driver3=create_driver(name="Johnny", surname="Doe", nickname="johnnydoe")

        driver4=create_driver(name="Ed", surname="Ed", nickname="ed")
        driver5=create_driver(name="Edd", surname="Edd", nickname="edd")
        driver6=create_driver(name="Eddy", surname="Eddy", nickname="eddy")

        response = self.client.get(reverse("history:driver_details", args=(driver1.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["related_drivers"], [driver2, driver3])