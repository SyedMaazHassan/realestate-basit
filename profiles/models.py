from django.db import models
from django.utils import timezone
# Create your models here.

class SocialProfile(models.Model):
    facebook = models.URLField()
    linkedin = models.URLField()
    twitter = models.URLField()

    def __str__(self):
        return self.facebook + ' ' + self.twitter + ' ' + self.linkedin

class Person(models.Model):
    profile_picture = models.ImageField(upload_to='dp/', default='dp/default-profile.png')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    social_profile = models.OneToOneField(SocialProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        abstract = True


class Agent(Person):
    tagline = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)



class TeamMember(Person):
    designation = models.CharField(max_length=255)