# Generated by Django 4.1.1 on 2023-06-21 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0010_paymentplan_offplansproperty_payment_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offplansproperty',
            name='payment_plan',
        ),
        migrations.DeleteModel(
            name='PaymentPlan',
        ),
    ]
