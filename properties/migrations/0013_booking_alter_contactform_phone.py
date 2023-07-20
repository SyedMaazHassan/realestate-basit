# Generated by Django 4.1.1 on 2023-07-20 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_paymentplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_type', models.CharField(max_length=255)),
                ('fromm', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='contactform',
            name='phone',
            field=models.CharField(max_length=16),
        ),
    ]
