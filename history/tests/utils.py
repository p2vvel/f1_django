"""
Contains functions written to make testing app easier
"""


from history.models import (
    Drivers,
    Circuits,
    Qualifying,
    Races,
    Results,
    Status,
    Constructors,
    Seasons,
)


def create_driver(name, surname, nickname="test_driver", code="TST", number=12, url=""):
    url = nickname if url == "" else url
    return Drivers.objects.create(
        name=name,
        surname=surname,
        nickname=nickname,
        code=code,
        number=number,
        wiki_url=url,
    )


def create_circuit(name, nickname="nickname", url=""):
    url = name.lower() + "_" + nickname if url == "" else url
    return Circuits.objects.create(name=name, nickname=nickname, wiki_url=url)


def create_constructor(name, nickname="test_constructor", url=""):
    url = name.lower() + "_" + nickname if url == "" else url
    return Constructors.objects.create(name=name, nickname=nickname, wiki_url=url)


def create_race(circuit, name, date, year=2013, round=7):
    return Races.objects.create(
        circuit=circuit, date=date, name=name, year=year, round=round
    )


def create_result(
    race,
    driver,
    constructor,
    status,
    grid=1,
    position=1,
    position_info=1,
    position_order=1,
    points=10,
    laps=50,
):
    return Results.objects.create(
        race=race,
        driver=driver,
        constructor=constructor,
        grid=grid,
        position_order=position_order,
        points=points,
        laps=laps,
        status=status,
        position_info=position_info,
        position=position,
    )


def create_status(status_info):
    return Status.objects.create(status_info=status_info)


def create_qualifying(race, driver, constructor, position, number):
    return Qualifying.objects.create(
        race=race,
        driver=driver,
        constructor=constructor,
        driver_number=number,
        position=position,
    )


def create_season(year, url=""):
    if url == "":
        url = "year_%s" % year
    return Seasons.objects.create(year=year, wiki_url=url)
