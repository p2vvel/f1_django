# Generated by Django 3.2.5 on 2021-07-25 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='circuits',
            old_name='circuitid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='circuits',
            old_name='circuitref',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='constructorresults',
            old_name='constructorid',
            new_name='constructor',
        ),
        migrations.RenameField(
            model_name='constructorresults',
            old_name='constructorresultsid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='constructorresults',
            old_name='raceid',
            new_name='race',
        ),
        migrations.RenameField(
            model_name='constructors',
            old_name='constructorid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='constructors',
            old_name='constructorref',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='constructorstandings',
            old_name='constructorid',
            new_name='constructor',
        ),
        migrations.RenameField(
            model_name='constructorstandings',
            old_name='constructorstandingsid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='constructorstandings',
            old_name='positiontext',
            new_name='position_info',
        ),
        migrations.RenameField(
            model_name='constructorstandings',
            old_name='raceid',
            new_name='race',
        ),
        migrations.RenameField(
            model_name='drivers',
            old_name='driverid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='drivers',
            old_name='forename',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='drivers',
            old_name='driverref',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='driverstandings',
            old_name='driverid',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='driverstandings',
            old_name='driverstandingsid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='driverstandings',
            old_name='positiontext',
            new_name='position_info',
        ),
        migrations.RenameField(
            model_name='driverstandings',
            old_name='raceid',
            new_name='race',
        ),
        migrations.RenameField(
            model_name='laptimes',
            old_name='driverid',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='laptimes',
            old_name='raceid',
            new_name='race',
        ),
        migrations.RenameField(
            model_name='pitstops',
            old_name='driverid',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='pitstops',
            old_name='raceid',
            new_name='race',
        ),
        migrations.RenameField(
            model_name='qualifying',
            old_name='constructorid',
            new_name='constructor',
        ),
        migrations.RenameField(
            model_name='qualifying',
            old_name='driverid',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='qualifying',
            old_name='qualifyid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='qualifying',
            old_name='raceid',
            new_name='race',
        ),
        migrations.RenameField(
            model_name='races',
            old_name='circuitid',
            new_name='circuit',
        ),
        migrations.RenameField(
            model_name='races',
            old_name='raceid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='constructorid',
            new_name='constructor',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='driverid',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='fastestlap',
            new_name='fastest_lap',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='fastestlapspeed',
            new_name='fastest_lapspeed',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='fastestlaptime',
            new_name='fastest_laptime',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='resultid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='positiontext',
            new_name='position_info',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='positionorder',
            new_name='position_order',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='raceid',
            new_name='race',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='statusid',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='statusid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='status',
            new_name='status_info',
        ),
        migrations.AlterUniqueTogether(
            name='laptimes',
            unique_together={('race', 'driver', 'lap')},
        ),
        migrations.AlterUniqueTogether(
            name='pitstops',
            unique_together={('race', 'driver', 'stop')},
        ),
    ]
