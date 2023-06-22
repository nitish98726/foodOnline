# Generated by Django 4.2.2 on 2023-06-22 08:08

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_userprofile_address_line1_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=4326
            ),
        ),
    ]
