"""
Contains functions written to make testing app easier
"""

from django import test
from django.db import reset_queries
from history.models import *


def assert_grouped_elements(test_class, data_a, data_b):
    '''
    Prostsze testowanie struktur zwroconych przez funkcje history.models.utils.group_elements
    '''
    test_class.assertEqual(len(data_a), len(data_b))
    temp = zip(sorted(data_a), sorted(data_b))
    for a, b in temp:
        test_class.assertEqual(a[0], b[0])  #pierwszy element zawsze jest pojedyncza wartoscia
        test_class.assertCountEqual(a[1], b[1]) #drugi element zawsze jest lista


#yapf:disable
def create_driver(name,surname, nickname="test_driver",code="TST",number=12, url=""):
    url = nickname if url == "" else url
    return Drivers.objects.create(name=name,surname=surname,nickname=nickname,
                                    code=code,number=number,wiki_url=url)
#yapf:enable


def create_circuit(name, nickname="nickname", url=""):
    url = name.lower() + "_" + nickname if url == "" else url
    return Circuits.objects.create(name=name, nickname=nickname, wiki_url=url)


def create_constructor(name, nickname="test_constructor", url=""):
    url = name.lower() + "_" + nickname if url == "" else url
    return Constructors.objects.create(name=name,
                                       nickname=nickname,
                                       wiki_url=url)


def create_race(circuit, name, date, year=2013, round=7):
    return Races.objects.create(circuit=circuit,
                                date=date,
                                name=name,
                                year=year,
                                round=round)


#yapf: disable
def create_result(race,driver,constructor,status,grid=1,position=1, position_info=1,position_order=1, points=10, laps=50):
    return Results.objects.create(
        race=race, driver=driver,constructor=constructor, grid=grid,
        position_order=position_order, points=points, laps=laps,
        status=status, position_info=position_info,position=position)
#yapf:enable


def create_status(status_info):
    return Status.objects.create(status_info=status_info)


def create_qualifying(race, driver, constructor, position, number):
    return Qualifying.objects.create(race=race,
                                     driver=driver,
                                     constructor=constructor,
                                     driver_number=number,
                                     position=position)


def create_season(year, url=""):
    if url == "":
        url = "year_%s" % year
    return Seasons.objects.create(year=year, wiki_url=url)


def create_driverstandings(driver, race, points=25, position=1, wins=1):
    return Driverstandings.objects.create(driver=driver,
                                          race=race,
                                          points=points,
                                          position=position,
                                          wins=wins)


#yapf: disable
def create_constructorstandings(constructor, race, points=25, position=1, wins=1):
    return Constructorstandings.objects.create(
                                        constructor=constructor,
                                        race=race,
                                        points=points,
                                        position=position,
                                        wins=wins)
#yapf: enable