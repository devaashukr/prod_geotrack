# Generated by Django 4.2.5 on 2023-10-04 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_operatorbusses"),
        ("geotrack", "0004_geodevdetails_operator_bus_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="GeoDevDetails",
            new_name="GeoDevDetail",
        ),
    ]
