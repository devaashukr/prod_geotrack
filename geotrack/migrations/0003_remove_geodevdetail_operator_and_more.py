# Generated by Django 4.2.5 on 2023-10-06 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("geotrack", "0002_alter_geodevdetail_operator_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="geodevdetail",
            name="operator",
        ),
        migrations.RemoveField(
            model_name="geodevdetail",
            name="operatorbus",
        ),
    ]
