# Generated by Django 4.1.1 on 2023-05-12 11:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.URLField()),
                ('linkedin', models.URLField()),
                ('twitter', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(default='dp/default-profile.png', upload_to='dp/')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('designation', models.CharField(max_length=255)),
                ('social_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.socialprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(default='dp/default-profile.png', upload_to='dp/')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('tagline', models.CharField(max_length=255)),
                ('overview', models.TextField(blank=True, null=True)),
                ('social_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.socialprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
