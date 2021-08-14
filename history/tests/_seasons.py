from datetime import datetime, timedelta
from .utils import *
from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase, client


class SeasonViewTests(TestCase):
    
    def test_races_count_finished_current_season(self):
        season = create_season(year=2021)
        circuit = create_circuit(name="Monza", nickname="monza")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        #yapf: enable
        races = []
        days = [-7, -6, -5, -4, -3, -2, -1]
        for k in range(len(days)):
            races.append(
                create_race(circuit=circuit,
                            name="Race%s" % (k + 1),
                            year=2021,
                            round=k + 1,
                            date=datetime.now() + timedelta(days=days[k])))
        #yapf: disable
        driver_standings = []
        for k in races:
            driver_standings.append(create_driverstandings(driver=drivers[0], race=k, points=25, position=1, wins=1))
            driver_standings.append(create_driverstandings(driver=drivers[1], race=k, points=18, position=2, wins=0))
            driver_standings.append(create_driverstandings(driver=drivers[2], race=k, points=15, position=3, wins=0))
        #yapf: enable
        response = self.client.get(
            reverse("history:season_details", args=(season.year, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seasons.count_races(2021), 7)
        self.assertEqual(Seasons.count_total_races(2021), 7)
        self.assertEqual(Seasons.season_finished(2021), True)
        self.assertEqual(Seasons.get_latest_race(2021), races[-1])

    def test_races_count_unfinished_current_season(self):
        season = create_season(year=2021)
        circuit = create_circuit(name="Monza", nickname="monza")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        #yapf: enable
        races = []
        days = [-7, -6, -5, -4, -3, -2, -1]
        for k in range(len(days)):
            races.append(
                create_race(circuit=circuit,
                            name="Race%s" % (k + 1),
                            year=2021,
                            round=k + 1,
                            date=datetime.now() + timedelta(days=days[k])))
        #yapf: disable
        driver_standings = []
        for k in races[:-2]:
            driver_standings.append(create_driverstandings(driver=drivers[0], race=k, points=25, position=1, wins=1))
            driver_standings.append(create_driverstandings(driver=drivers[1], race=k, points=18, position=2, wins=0))
            driver_standings.append(create_driverstandings(driver=drivers[2], race=k, points=15, position=3, wins=0))
        #yapf: enable

        response = self.client.get(
            reverse("history:season_details", args=(season.year, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seasons.count_races(2021), 5)
        self.assertEqual(Seasons.count_total_races(2021), 7)
        self.assertEqual(Seasons.season_finished(2021), False)
        self.assertEqual(Seasons.get_latest_race(2021), races[4])

    def test_races_count_unfinished_current_season2(self):
        season = create_season(year=2021)
        circuit = create_circuit(name="Monza", nickname="monza")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        #yapf: enable
        races = []
        days = [-7, -6, -5, -4, -3, -2, -1]
        for k in range(len(days)):
            races.append(
                create_race(circuit=circuit,
                            name="Race%s" % (k + 1),
                            year=2021,
                            round=k + 1,
                            date=datetime.now() + timedelta(days=days[k])))
        #yapf: disable
        driver_standings = []
        for k in races[:1]:
            driver_standings.append(create_driverstandings(driver=drivers[0], race=k, points=25, position=1, wins=1))
            driver_standings.append(create_driverstandings(driver=drivers[1], race=k, points=18, position=2, wins=0))
            driver_standings.append(create_driverstandings(driver=drivers[2], race=k, points=15, position=3, wins=0))
        #yapf: enable

        response = self.client.get(
            reverse("history:season_details", args=(season.year, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seasons.count_races(2021), 1)
        self.assertEqual(Seasons.count_total_races(2021), 7)
        self.assertEqual(Seasons.season_finished(2021), False)
        self.assertEqual(Seasons.get_latest_race(2021), races[0])

    def test_races_count_unfinished_current_season_no_races(self):
        season = create_season(year=2021)
        circuit = create_circuit(name="Monza", nickname="monza")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        #yapf: enable
        races = []
        days = [-7, -6, -5, -4, -3, -2, -1]
        for k in range(len(days)):
            races.append(
                create_race(circuit=circuit,
                            name="Race%s" % (k + 1),
                            year=2021,
                            round=k + 1,
                            date=datetime.now() + timedelta(days=days[k])))

        response = self.client.get(
            reverse("history:season_details", args=(season.year, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seasons.count_races(2021), 0)
        self.assertEqual(Seasons.count_total_races(2021), 7)
        self.assertEqual(Seasons.season_finished(2021), False)
        self.assertEqual(Seasons.get_latest_race(2021), None)

    def test_season_no_races(self):
        season = create_season(year=2021)

        response = self.client.get(
            reverse("history:season_details", args=(season.year, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seasons.count_races(2021), 0)
        self.assertEqual(Seasons.count_total_races(2021), 0)
        self.assertEqual(Seasons.season_finished(2021), False)
        self.assertEqual(Seasons.get_latest_race(2021), None)

    def test_races_count_finished_current_season(self):
        season = create_season(year=2021)
        circuit = create_circuit(name="Monza", nickname="monza")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        #yapf: enable
        races = []
        days = [-7, -6, -5, -4, -3, -2, -1]
        for k in range(len(days)):
            races.append(
                create_race(circuit=circuit,
                            name="Race%s" % (k + 1),
                            year=2021,
                            round=k + 1,
                            date=datetime.now() + timedelta(days=days[k])))
        #yapf: disable
        driver_standings = []
        for k in races:
            driver_standings.append(create_driverstandings(driver=drivers[0], race=k, points=25, position=1, wins=1))
            driver_standings.append(create_driverstandings(driver=drivers[1], race=k, points=18, position=2, wins=0))
            driver_standings.append(create_driverstandings(driver=drivers[2], race=k, points=15, position=3, wins=0))
        #yapf: enable

        response = self.client.get(
            reverse("history:season_details", args=(season.year, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seasons.count_races(2021), 7)
        self.assertEqual(Seasons.count_total_races(2021), 7)
        self.assertEqual(Seasons.season_finished(2021), True)
        self.assertEqual(Seasons.get_latest_race(2021), races[-1])

    