# Generated by Django 4.2.2 on 2023-08-03 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_total_data_order_vendors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="tax_data",
            field=models.JSONField(
                blank=True,
                help_text="Data Format:{'tax_type':{'tax_percentage':'tax_amount'}}",
                null=True,
            ),
        ),
    ]
