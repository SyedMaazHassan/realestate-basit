# Generated by Django 4.1.1 on 2023-07-20 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0014_homepagesites'),
    ]

    operations = [
        migrations.AddField(
            model_name='offplansproperty',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offplansproperty',
            name='property_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]