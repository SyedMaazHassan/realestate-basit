# Generated by Django 4.1.1 on 2023-10-19 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0017_machineinfo_dataupdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machineinfo',
            name='user_agent',
        ),
        migrations.AddField(
            model_name='dataupdate',
            name='update_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='machineinfo',
            name='ip_address',
            field=models.CharField(max_length=100),
        ),
    ]
