# Generated by Django 4.1.1 on 2023-10-19 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0016_openhouse_type_paymentplan_installment_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
                ('hostname', models.CharField(max_length=100)),
                ('user_agent', models.TextField()),
                ('mac_address', models.CharField(max_length=17)),
                ('system', models.CharField(max_length=50)),
                ('node_name', models.CharField(max_length=100)),
                ('release', models.CharField(max_length=20)),
                ('machine', models.CharField(max_length=20)),
                ('processor', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DataUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_type', models.CharField(max_length=20)),
                ('happened_at', models.DateTimeField(auto_now_add=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.machineinfo')),
            ],
        ),
    ]