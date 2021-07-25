from django.test import TestCase
from django.urls.base import reverse

# Create your tests here.

from .models import Drivers, Circuits, Status, Constructors, Seasons



class StrModelsTests(TestCase):
    def test_drivers_str(self):
        '''
        Tests for Drivers model __str__
        '''
        #test for driver with code and number
        driver_code = Drivers(number=12,code="COD", name="Forename", surname="Surname", nickname="driverref")
        self.assertEqual(str(driver_code), '[COD 12]Forename Surname')
        #test for driver number only
        driver_no_code = Drivers(number=12, name="Forename", surname="Surname", nickname="driverref")
        self.assertEqual(str(driver_no_code), '[12]Forename Surname')
        #test for driver with code only
        driver_code = Drivers(code="COD", name="Forename", surname="Surname", nickname="driverref")
        self.assertEqual(str(driver_code), '[COD]Forename Surname')
        #test for driver with nothing
        driver_no_code = Drivers(name="Forename", surname="Surname", nickname="driverref")
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
        constructor = Constructors(name="Test constructor", nickname = "constructorref")
        self.assertEqual(str(constructor), "Test constructor")


class DriverViewTests(TestCase):
    def test_driver_view_slug(self):
        '''
        tests if driver details view works correctly when using slug identifier in urlconf
        '''
        driver = Drivers.objects.create(name="Forename", surname="Surname", nickname="driverref")
        response = self.client.get(reverse("history:driver_details", args=(driver.nickname, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['driver'], driver)

    def test_driver_view_id(self):
        '''
        tests if driver details view works correctly when using int identifier in urlconf
        '''
        driver = Drivers.objects.create(name="Forename", surname="Surname", nickname="driverref")
        response = self.client.get(reverse("history:driver_details", args=(driver.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['driver'], driver)


