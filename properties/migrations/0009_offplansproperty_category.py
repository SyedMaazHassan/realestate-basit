# Generated by Django 4.1.1 on 2023-06-21 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_populararea'),
    ]

    operations = [
        migrations.AddField(
            model_name='offplansproperty',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Category'),
        ),
    ]
