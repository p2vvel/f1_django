from django.urls.base import reverse
from django.test import TestCase, client

from history.models import Drivers


class TestDriversView(TestCase):
    fixtures = ["post2000db.json"]

    def test_simple_view(self):
        '''
        Testuje tylko czy podstrony kierowcow dzialaja
        '''
        vettel = Drivers.objects.get(surname="Vettel")
        alonso = Drivers.objects.get(surname="Alonso")
        leclerc = Drivers.objects.get(surname="Leclerc")

        for driver in [vettel, alonso, leclerc]:
            response = self.client.get(reverse("history:driver_details", args=(driver.nickname,)))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["driver"], driver)
        