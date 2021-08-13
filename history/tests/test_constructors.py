from django.urls.base import reverse
from django.test import TestCase


from history.models import Constructors, Drivers


class ConstructorViewTests(TestCase):
    '''
    Testuje widok kierowcow na podstawie bazy zawierajacej informacje z lat 2000-2021(do GP UK)
    '''
    fixtures = ["post2000db.json"]

    def test_simple_view(self):
        '''
        Sprawdzam tylko, czy strona konstruktora sie wczytuje
        '''
        bmw_sauber = Constructors.objects.get(name="BMW Sauber")
        toro_rosso = Constructors.objects.get(name="Toro Rosso")
        red_bull = Constructors.objects.get(name="Red Bull")
        ferrari = Constructors.objects.get(name="Ferrari")
        aston_martin = Constructors.objects.get(name="Aston Martin")

        for constructor in [
                bmw_sauber, toro_rosso, red_bull, ferrari, aston_martin
        ]:
            response = self.client.get(
                reverse("history:constructor_details",
                        args=(constructor.nickname, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["constructor"], constructor)

    def test_drivers_per_season(self):
        '''
        Sprawdzam czy poprawnie pobieram informacje o kierowcach w danych sezonach w danym zespole
        '''
        
        red_bull = Constructors.objects.get(name="Red Bull")
        
        coulthard = Drivers.objects.get(surname="Coulthard")
        klien = Drivers.objects.get(surname="Klien")
        liuzzi = Drivers.objects.get(surname="Liuzzi")
        doornbos = Drivers.objects.get(surname="Doornbos")
        webber = Drivers.objects.get(surname="Webber")
        vettel = Drivers.objects.get(surname="Vettel")
        ricciardo = Drivers.objects.get(surname="Ricciardo")
        kvyat = Drivers.objects.get(surname="Kvyat")
        verstappen = Drivers.objects.get(surname="Verstappen", name="Max")
        albon = Drivers.objects.get(surname="Albon")
        gasly = Drivers.objects.get(surname="Gasly")
        perez = Drivers.objects.get(surname="Perez")

        red_bull_drivers = [(2005, [coulthard, klien, liuzzi]),
                            (2006, [coulthard, klien, doornbos]),
                            (2007, [coulthard, webber]),
                            (2008, [coulthard, webber]),
                            (2009, [webber, vettel]), (2010, [webber, vettel]),
                            (2011, [webber, vettel]), (2012, [webber, vettel]),
                            (2013, [webber, vettel]),
                            (2014, [ricciardo, vettel]),
                            (2015, [ricciardo, kvyat]),
                            (2016, [ricciardo, kvyat, verstappen]),
                            (2017, [ricciardo, verstappen]),
                            (2018, [ricciardo, verstappen]),
                            (2019, [verstappen, gasly, albon]),
                            (2020, [verstappen, albon]),
                            (2021, [verstappen, perez])]
        
        self.maxDiff = None

        for k in [(red_bull, red_bull_drivers)]:
            for team, drivers in k:
                response = self.client.get(reverse("history:constructor_details", args=(team.nickname,)))
                self.assertEqual(response.status_code, 200)
                self.assertCountEqual(response.context["drivers"], drivers)
