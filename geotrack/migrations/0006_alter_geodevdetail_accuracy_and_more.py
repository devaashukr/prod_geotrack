# Generated by Django 4.2.5 on 2023-10-04 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geotrack", "0005_rename_geodevdetails_geodevdetail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="geodevdetail",
            name="accuracy",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="altitude",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="attributes",
            field=models.CharField(default=0, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="course",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="network",
            field=models.CharField(default="tcp", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="servertime",
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]