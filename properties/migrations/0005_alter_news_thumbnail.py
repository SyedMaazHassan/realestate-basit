# Generated by Django 4.1.1 on 2023-05-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_alter_news_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='thumbnail',
            field=models.ImageField(blank=True, default='thumbnails/default-news.jpeg', null=True, upload_to='thumbnails'),
        ),
    ]
