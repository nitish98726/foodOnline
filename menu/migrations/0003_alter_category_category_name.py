# Generated by Django 4.2.2 on 2023-06-21 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0002_alter_category_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.CharField(max_length=50),
        ),
    ]