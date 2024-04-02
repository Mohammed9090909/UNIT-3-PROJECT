# Generated by Django 4.2.11 on 2024-04-01 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_place_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="category",
            field=models.CharField(
                choices=[("For Sale", "For Sale"), ("For Rent", "For Rent")],
                max_length=50,
            ),
        ),
    ]
