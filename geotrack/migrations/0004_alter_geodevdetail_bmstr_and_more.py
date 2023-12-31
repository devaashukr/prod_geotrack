# Generated by Django 4.2.5 on 2023-10-08 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geotrack", "0003_alter_geodevdetail_protocol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="geodevdetail",
            name="bmStr",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="exceptionBM",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="haltedSince",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="is_sent_traccar",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="locStr",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="movingSince",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="geodevdetail",
            name="noDataSince",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
