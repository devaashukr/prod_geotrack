# Generated by Django 4.2.5 on 2023-10-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0018_alter_operator_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operator",
            name="username",
            field=models.CharField(max_length=100),
        ),
    ]
