# Generated by Django 4.2.5 on 2023-10-03 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_operator_platform"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="operator",
            name="other",
        ),
    ]
