# Generated by Django 4.2.11 on 2024-04-01 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_remove_place_description_place_for_rent_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="image",
            field=models.ImageField(upload_to="images/"),
        ),
    ]