from datetime import timedelta
from history.models import Seasons
from django.urls.base import reverse
from django.test import TestCase

from .utils import *


class SeasonViewTests(TestCase):
    fixtures = ["post2000db.json"]

    def test_simple_view(self):
        '''
        Sprawdzam tylko czy prawidlowo laduje podstrone sezonu
        '''
        seasons = [
            Seasons.objects.get(year=year) for year in range(2000, 2022)
        ]

        for season in seasons:
            response = self.client.get(
                reverse("history:season_details", args=(season.year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["season"], season)

    def test_count_total_races(self):
        '''
        Sprawdzam czy prawidlowo pobieram informacje na tematy calkowitej liczby wyscigow w danym sezonie
        '''

        seasons = [
            Seasons.objects.get(year=year)
            for year in [2004, 2005, 2007, 2010, 2013, 2016, 2021]
        ]
        #calkowita liczba wyscigow w adanym sezonie
        seasons_total_races = [18, 19, 17, 19, 19, 21, 23]

        for season, total_races in zip(seasons, seasons_total_races):
            response = self.client.get(
                reverse("history:season_details", args=(season.year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["total_races"], total_races)

    def test_count_races(self):
        '''
        Sprawdzam czy prawidlowo pobieram informacje na temat dotychczas zorganizowanych wyscigow w danym sezonie
        '''
        seasons = [
            Seasons.objects.get(year=year)
            for year in [2004, 2005, 2007, 2010, 2013, 2016, 2021]
        ]
        #odbyta liczba wyscigow w danym sezonie
        seasons_races = [18, 19, 17, 19, 19, 21, 10]

        for season, organized_races in zip(seasons, seasons_races):
            response = self.client.get(
                reverse("history:season_details", args=(season.year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["organized_races"],
                             organized_races)

    def test_season_finished(self):
        '''
        Sprawdzam czy prawdilowo okreslam ze sezon jest juz zakonczony
        '''
        seasons = [
            Seasons.objects.get(year=year)
            for year in [2004, 2005, 2007, 2010, 2013, 2016, 2021]
        ]

        seasons_finished = [True, True, True, True, True, True, False]

        for season, finished in zip(seasons, seasons_finished):
            response = self.client.get(
                reverse("history:season_details", args=(season.year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["finished"], finished)

    def test_next_season(self):
        '''
        Sprawdzam czy porpawnie pobieram informacje o nastepnym sezonie(przy ostatnim w bazie ma nic nie byc)
        '''
        seasons = list(Seasons.objects.all().order_by("year")) + [None]

        for k in range(1, len(seasons)):
            response = self.client.get(
                reverse("history:season_details",
                        args=(seasons[k - 1].year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["next_season"], seasons[k])

    def test_previous_season(self):
        '''
        Sprawdzam czy porpawnie pobieram informacje o poprzednim sezonie(przy ostatnim w bazie ma nic nie byc)
        '''
        seasons = [None] + list(Seasons.objects.all().order_by("year"))

        for k in range(1, len(seasons)):
            response = self.client.get(
                reverse("history:season_details", args=(seasons[k].year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["previous_season"],
                             seasons[k - 1])

    def test_drivers(self):
        '''
        Sprawdzam czy prawidlowo pobieram informacje o kierowcach
        '''
        season_2013 = Seasons.objects.get(year=2013)
        drivers_names_2013 = (("Sebastian", "Vettel"), ("Fernando", "Alonso"),
                              ("Mark", "Webber"), ("Lewis", "Hamilton"),
                              ("Kimi", "Räikkönen"), ("Nico", "Rosberg"),
                              ("Romain", "Grosjean"), ("Felipe", "Massa"),
                              ("Jenson", "Button"), ("Nico", "Hülkenberg"),
                              ("Sergio", "Pérez"), ("Paul", "di Resta"),
                              ("Adrian", "Sutil"), ("Daniel",
                                                    "Ricciardo"), ("Jean-Éric",
                                                                   "Vergne"),
                              ("Esteban", "Gutiérrez"), ("Valtteri", "Bottas"),
                              ("Pastor", "Maldonado"), ("Jules", "Bianchi"),
                              ("Charles", "Pic"), ("Giedo", "van der Garde"),
                              ("Heikki", "Kovalainen"), ("Max", "Chilton"))

        drivers_2013 = [
            Drivers.objects.get(surname=surname, name=name)
            for (name, surname) in drivers_names_2013
        ]

        season_2021 = Seasons.objects.get(year=2021)
        drivers_names_2021 = (("Max", "Verstappen"), ("Lewis", "Hamilton"),
                              ("Lando", "Norris"), ("Valtteri", "Bottas"),
                              ("Sergio", "Pérez"), ("Charles", "Leclerc"),
                              ("Carlos", "Sainz"), ("Daniel", "Ricciardo"),
                              ("Pierre", "Gasly"), ("Sebastian", "Vettel"),
                              ("Fernando", "Alonso"), ("Lance", "Stroll"),
                              ("Esteban", "Ocon"), ("Yuki", "Tsunoda"),
                              ("Kimi", "Räikkönen"), ("Antonio", "Giovinazzi"),
                              ("George", "Russell"), ("Mick", "Schumacher"),
                              ("Nicholas", "Latifi"), ("Nikita", "Mazepin"))

        drivers_2021 = [
            Drivers.objects.get(surname=surname, name=name)
            for (name, surname) in drivers_names_2021
        ]

        for season, drivers in ((season_2013, drivers_2013), (season_2021,
                                                              drivers_2021)):
            response = self.client.get(
                reverse("history:season_details", args=(season.year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual([k.driver for k in response.context["drivers"]],
                             drivers)

    def test_constructors(self):
        '''
        Sprawdzam czy prawidlowo pobieram informacje o konstruktorach
        '''
        season_2013 = Seasons.objects.get(year=2013)
        constructors_names_2013 = ("Red Bull", "Mercedes", "Ferrari",
                                   "Lotus F1", "McLaren", "Force India",
                                   "Sauber", "Toro Rosso", "Williams",
                                   "Marussia", "Caterham")

        constructors_2013 = [
            Constructors.objects.get(name=name)
            for name in constructors_names_2013
        ]

        season_2021 = Seasons.objects.get(year=2021)
        constructors_names_2021 = ("Red Bull", "Mercedes", "McLaren",
                                   "Ferrari", "AlphaTauri", "Aston Martin",
                                   "Alpine F1 Team", "Alfa Romeo", "Williams",
                                   "Haas F1 Team")
        constructors_2021 = [
            Constructors.objects.get(name=name)
            for name in constructors_names_2021
        ]

        for season, constructors in ((season_2013, constructors_2013),
                                     (season_2021, constructors_2021)):
            response = self.client.get(
                reverse("history:season_details", args=(season.year, )))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                [k.constructor for k in response.context["constructors"]],
                constructors)


class SeasonViewTestsFakeData(TestCase):
    '''
    Testy napisane w celu sprawdzenia zachowania w przypadku roznych wariantow aktualnego sezonu
    '''
    def test_races_count_finished_current_season(self):
        season = create_season(year=2021)
        circuit = create_circuit(name="Monza", nickname="monza")
        status = create_status("Finished")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        constructors = [
            create_constructor(name="Red Bull", nickname="redbull"),
            create_constructor(name="Ferrari", nickname="ferrari"),
            create_constructor(name="McLaren", nickname="mclaren")
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
        results = []
        for k in races:
            results.append(create_result(race=k, driver=drivers[0], constructor=constructors[0], status=status)),
            results.append(create_result(race=k, driver=drivers[1], constructor=constructors[1], status=status)),
            results.append(create_result(race=k, driver=drivers[2], constructor=constructors[2], status=status)),
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
        status = create_status("Finished")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        constructors = [
            create_constructor(name="Red Bull", nickname="redbull"),
            create_constructor(name="Ferrari", nickname="ferrari"),
            create_constructor(name="McLaren", nickname="mclaren")
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
        results = []
        for k in races[:-2]:
            results.append(create_result(race=k, driver=drivers[0], constructor=constructors[0], status=status)),
            results.append(create_result(race=k, driver=drivers[1], constructor=constructors[1], status=status)),
            results.append(create_result(race=k, driver=drivers[2], constructor=constructors[2], status=status)),
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
        status = create_status("Finished")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        constructors = [
            create_constructor(name="Red Bull", nickname="redbull"),
            create_constructor(name="Ferrari", nickname="ferrari"),
            create_constructor(name="McLaren", nickname="mclaren")
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
        results = []
        for k in races[:1]:
            results.append(create_result(race=k, driver=drivers[0], constructor=constructors[0], status=status)),
            results.append(create_result(race=k, driver=drivers[1], constructor=constructors[1], status=status)),
            results.append(create_result(race=k, driver=drivers[2], constructor=constructors[2], status=status)),
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
        status = create_status("Finished")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        constructors = [
            create_constructor(name="Red Bull", nickname="redbull"),
            create_constructor(name="Ferrari", nickname="ferrari"),
            create_constructor(name="McLaren", nickname="mclaren")
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
        status = create_status("Finished")
        #yapf: disable
        drivers = [
            create_driver(name="Sebastian",surname="Vettel",nickname="vettel"),
            create_driver(name="Fernando", surname="Alonso",nickname="alonso"),
            create_driver(name="Kimi", surname="Raikkonen", nickname="kimi"),
        ]
        constructors = [
            create_constructor(name="Red Bull", nickname="redbull"),
            create_constructor(name="Ferrari", nickname="ferrari"),
            create_constructor(name="McLaren", nickname="mclaren")
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
        results = []
        for k in races:
            results.append(create_result(race=k, driver=drivers[0], constructor=constructors[0], status=status)),
            results.append(create_result(race=k, driver=drivers[1], constructor=constructors[1], status=status)),
            results.append(create_result(race=k, driver=drivers[2], constructor=constructors[2], status=status)),
        #yapf: enable

        response = self.client.get(
            reverse("history:season_details", args=(season.year, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seasons.count_races(2021), 7)
        self.assertEqual(Seasons.count_total_races(2021), 7)
        self.assertEqual(Seasons.season_finished(2021), True)
        self.assertEqual(Seasons.get_latest_race(2021), races[-1])
