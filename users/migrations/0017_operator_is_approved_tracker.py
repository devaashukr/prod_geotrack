# Generated by Django 4.2.5 on 2023-10-04 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0016_remove_operator_tracker_approved_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="operator",
            name="is_approved_tracker",
            field=models.BooleanField(default=False),
        ),
    ]
