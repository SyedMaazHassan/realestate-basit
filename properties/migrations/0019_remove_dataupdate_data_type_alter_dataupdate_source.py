# Generated by Django 4.1.1 on 2023-10-19 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0018_remove_machineinfo_user_agent_dataupdate_update_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataupdate',
            name='data_type',
        ),
        migrations.AlterField(
            model_name='dataupdate',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='properties.machineinfo'),
        ),
    ]
