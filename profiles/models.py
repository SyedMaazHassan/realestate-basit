from django.db import models
from django.utils import timezone
# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class SocialProfile(models.Model):
    facebook = models.URLField()
    linkedin = models.URLField()
    twitter = models.URLField()

    def __str__(self):
        return self.facebook + ' ' + self.twitter + ' ' + self.linkedin

class Person(models.Model):
    profile_picture = models.ImageField(upload_to='dp/', default='dp/default-profile.png')
    email = models.EmailField(null=True, blank=True)
    social_profile = models.OneToOneField(SocialProfile, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class TeamMember(Person):
    designation = models.CharField(max_length=255)


class AgentProfile(Person):
    crm_id = models.IntegerField()
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.name