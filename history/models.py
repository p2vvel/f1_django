# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Drivers(models.Model):
    id = models.AutoField(db_column="driverId", primary_key=True)
    nickname = models.CharField(db_column="driverRef", max_length=255)
    number = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birthday = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    wiki_url = models.CharField(unique=True, max_length=255)

    def __str__(self):
        if self.code or self.number:
            return (
                "[{}{}{}]".format(
                    "%s" % self.code if self.code else "",
                    " " if self.code and self.number else "",
                    "%s" % self.number if self.number else "",
                )
                + "%s %s" % (self.name, self.surname)
            )
        else:
            return "%s %s" % (self.name, self.surname)

    class Meta:
        db_table = "drivers"


class Circuits(models.Model):
    id = models.AutoField(db_column="circuitId", primary_key=True)
    nickname = models.CharField(db_column="circuitRef", max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    alt = models.IntegerField(blank=True, null=True)
    wiki_url = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "circuits"


class Constructors(models.Model):
    id = models.AutoField(db_column="constructorId", primary_key=True)
    nickname = models.CharField(db_column="constructorRef", max_length=255)
    name = models.CharField(unique=True, max_length=255)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    wiki_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "constructors"


class Constructorresults(models.Model):
    id = models.AutoField(db_column="constructorResultsId", primary_key=True)
    race = models.ForeignKey("Races", models.DO_NOTHING, db_column="raceId")
    constructor = models.ForeignKey(
        "Constructors", models.DO_NOTHING, db_column="constructorId"
    )
    points = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "constructorResults"


class Constructorstandings(models.Model):
    id = models.AutoField(db_column="constructorStandingsId", primary_key=True)
    race = models.ForeignKey("Races", models.DO_NOTHING, db_column="raceId")
    constructor = models.ForeignKey(
        "Constructors", models.DO_NOTHING, db_column="constructorId"
    )
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    position_info = models.CharField(
        db_column="positionText", max_length=255, blank=True, null=True
    )
    wins = models.IntegerField()

    class Meta:
        db_table = "constructorStandings"


class Driverstandings(models.Model):
    id = models.AutoField(db_column="driverStandingsId", primary_key=True)
    race = models.ForeignKey("Races", models.DO_NOTHING, db_column="raceId")
    driver = models.ForeignKey("Drivers", models.DO_NOTHING, db_column="driverId")
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    position_info = models.CharField(
        db_column="positionText", max_length=255, blank=True, null=True
    )
    wins = models.IntegerField()

    class Meta:
        db_table = "driverStandings"


class Laptimes(models.Model):
    race = models.OneToOneField(
        "Races", models.DO_NOTHING, db_column="raceId", primary_key=True
    )
    driver = models.ForeignKey(Drivers, models.DO_NOTHING, db_column="driverId")
    lap = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    milliseconds = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "lapTimes"
        unique_together = (("race", "driver", "lap"),)


class Pitstops(models.Model):
    race = models.OneToOneField(
        "Races", models.DO_NOTHING, db_column="raceId", primary_key=True
    )
    driver = models.ForeignKey(Drivers, models.DO_NOTHING, db_column="driverId")
    stop = models.IntegerField()
    lap = models.IntegerField()
    time = models.TimeField()
    duration = models.CharField(max_length=255, blank=True, null=True)
    milliseconds = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "pitStops"
        unique_together = (("race", "driver", "stop"),)


class Qualifying(models.Model):
    id = models.AutoField(db_column="qualifyId", primary_key=True)
    race = models.ForeignKey("Races", models.DO_NOTHING, db_column="raceId")
    driver = models.ForeignKey(Drivers, models.DO_NOTHING, db_column="driverId")
    constructor = models.ForeignKey(
        Constructors, models.DO_NOTHING, db_column="constructorId"
    )
    number = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    q1 = models.CharField(max_length=255, blank=True, null=True)
    q2 = models.CharField(max_length=255, blank=True, null=True)
    q3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "qualifying"


class Races(models.Model):
    id = models.AutoField(db_column="raceId", primary_key=True)
    year = models.IntegerField()
    round = models.IntegerField()
    circuit = models.ForeignKey(Circuits, models.DO_NOTHING, db_column="circuitId")
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    wiki_url = models.CharField(unique=True, max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "races"


class Results(models.Model):
    id = models.AutoField(db_column="resultId", primary_key=True)
    race = models.ForeignKey(Races, models.DO_NOTHING, db_column="raceId")
    driver = models.ForeignKey(Drivers, models.DO_NOTHING, db_column="driverId")
    constructor = models.ForeignKey(
        Constructors, models.DO_NOTHING, db_column="constructorId"
    )
    number = models.IntegerField(blank=True, null=True)
    grid = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    position_info = models.CharField(db_column="positionText", max_length=255)
    position_order = models.IntegerField(db_column="positionOrder")
    points = models.FloatField()
    laps = models.IntegerField()
    time = models.CharField(max_length=255, blank=True, null=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    fastest_lap = models.IntegerField(db_column="fastestLap", blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    fastest_laptime = models.CharField(
        db_column="fastestLapTime", max_length=255, blank=True, null=True
    )
    fastest_lapspeed = models.CharField(
        db_column="fastestLapSpeed", max_length=255, blank=True, null=True
    )
    status = models.ForeignKey("Status", models.DO_NOTHING, db_column="statusId")

    class Meta:
        db_table = "results"


class Seasons(models.Model):
    year = models.IntegerField(primary_key=True)
    wiki_url = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return "Season %s" % self.year

    class Meta:
        db_table = "seasons"


class Status(models.Model):
    id = models.AutoField(db_column="statusId", primary_key=True)
    status_info = models.CharField(max_length=255)

    def __str__(self):
        return self.status_test

    class Meta:
        db_table = "status"
