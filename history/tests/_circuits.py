from .utils import *
from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase, client
from datetime import datetime

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

        race1 = create_race(
            circuit=circuit, name="Race1", date=datetime.now(), round=2, year=2012
        )
        race2 = create_race(
            circuit=circuit, name="Race2", date=datetime.now(), round=2, year=2013
        )
        race3 = create_race(
            circuit=circuit2, name="Race3", date=datetime.now(), round=2, year=2014
        )
        race4 = create_race(
            circuit=circuit, name="Race4", date=datetime.now(), round=2, year=2015
        )
        race5 = create_race(
            circuit=circuit, name="Race5", date=datetime.now(), round=3, year=2015
        )

        response = self.client.get(
            reverse("history:circuit_details", args=(circuit.nickname,))
        )
        self.assertEqual(response.status_code, 200)

        expected_result = [(2012, [race1]), (2013, [race2]), (2015, [race4, race5])]

        self.assertCountEqual(response.context["races"], expected_result)
