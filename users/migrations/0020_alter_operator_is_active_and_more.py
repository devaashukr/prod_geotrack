# Generated by Django 4.2.5 on 2023-10-05 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0019_alter_operator_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operator",
            name="is_active",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="operator",
            name="is_approved_tracker",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
