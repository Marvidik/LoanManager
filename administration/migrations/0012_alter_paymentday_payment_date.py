# Generated by Django 4.1 on 2023-09-28 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0011_remove_paid_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentday',
            name='payment_date',
            field=models.DateField(),
        ),
    ]
