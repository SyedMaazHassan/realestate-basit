# Generated by Django 4.1.1 on 2023-06-21 19:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_agentprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='last_name',
        ),
        migrations.AddField(
            model_name='agentprofile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='agentprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='agentprofile',
            name='profile_picture',
            field=models.ImageField(default='dp/default-profile.png', upload_to='dp/'),
        ),
        migrations.AlterField(
            model_name='agentprofile',
            name='social_profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.socialprofile'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='social_profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.socialprofile'),
        ),
        migrations.DeleteModel(
            name='Agent',
        ),
    ]