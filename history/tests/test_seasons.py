from .utils import *
from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase, client

class SeasonViewTests(TestCase):
    def test_season_view_simple(self):
        season = create_season(year=2013)
        response = self.client.get(reverse("history:season_details", args=(season.year,)))
        self.assertEqual(response.status_code, 200)