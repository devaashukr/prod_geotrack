# Generated by Django 4.2.5 on 2023-10-08 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geotrack", "0002_remove_geodevdetail_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="geodevdetail",
            name="protocol",
            field=models.CharField(default="TCP", null=True),
        ),
    ]