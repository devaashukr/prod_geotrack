# Generated by Django 4.2.5 on 2023-10-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_remove_operator_other"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operator",
            name="password",
            field=models.CharField(editable=False, max_length=100),
        ),
    ]
