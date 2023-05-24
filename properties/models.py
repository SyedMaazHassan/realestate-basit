from django.db import models
from django.utils import timezone
from profiles.models import Agent
from django_quill.fields import QuillField
from rest_framework_api_key.models import AbstractAPIKey


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

class APIKey(AbstractAPIKey):
    name = models.CharField(max_length=255)

# class Price(models.Model):
#     property = models.OneToOneField('properties.OffPlansProperty', related_name='price', on_delete=models.CASCADE, blank=True, null=True)
#     land_department_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     trustee_office_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     mortgage_registration = models.DecimalField(max_digits=10, decimal_places=2)
#     real_estate_agency_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     tax_in_percent = models.DecimalField(max_digits=5, decimal_places=2)
#     bank_arrangement_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     valuation = models.DecimalField(max_digits=10, decimal_places=2)
#     conveyancing_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     total_purchase_costs = models.DecimalField(max_digits=10, decimal_places=2)
#     total_required_upfront = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.total_purchase_costs}'


# class PropertyDetail(models.Model):
#     property = models.OneToOneField('properties.OffPlansProperty', related_name='property_details', on_delete=models.CASCADE, blank=True, null=True)
#     rooms = models.IntegerField()
#     bathrooms = models.IntegerField()
#     kitchen = models.IntegerField()
#     floor = models.IntegerField()
#     size = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.size} sqft - {self.rooms} rooms - {self.bathrooms} bathrooms'


# class OffPlansProperty(models.Model):
#     SALE = 'SALE'
#     RENT = 'RENT'
#     STATUS_CHOICES = [
#         (SALE, 'For Sale'),
#         (RENT, 'For Rent'),
#     ]

#     ref_no = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     overview = models.TextField(null=True, blank=True)
#     mortgage_period = models.IntegerField()
#     deposit = models.DecimalField(max_digits=10, decimal_places=2)
#     interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
#     loan = models.DecimalField(max_digits=10, decimal_places=2)
#     monthly_repayments = models.DecimalField(max_digits=10, decimal_places=2)
#     agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
#     status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=SALE)
#     amenities = models.ManyToManyField(Amenity)
#     is_verified = models.BooleanField(default=False)
#     is_new = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.name
    



class Amenity(models.Model):
    icon = models.CharField(max_length=50, verbose_name='Icon')
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name


class OffPlansProperty(models.Model):
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Title')
    subtitle = models.CharField(max_length=255, verbose_name='Subtitle')
    description = QuillField(verbose_name='Description')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Minimum Price')
    max_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Maximum Price')
    developer = models.CharField(max_length=255, verbose_name='Developer')
    project_company_logo = models.ImageField(upload_to='project_company_logos/', verbose_name='Project Company Logo')
    handover_date = models.DateField(verbose_name='Handover Date')
    broucher = models.FileField(upload_to='brochures/', null=True, blank=True, verbose_name='Brochure')
    youtube_video_link = models.URLField(verbose_name='YouTube Video Link')
    amenities = models.ManyToManyField('Amenity', verbose_name='Amenities')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Location(models.Model):
    property = models.OneToOneField(OffPlansProperty, on_delete=models.CASCADE, related_name='location')
    address = models.CharField(max_length=255, verbose_name='Address')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='Longitude')

    def __str__(self):
        return self.address


class Gallery(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    PDF = 'pdf'
    TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (PDF, 'PDF'),
    ]

    property = models.ForeignKey(OffPlansProperty, on_delete=models.CASCADE, related_name="gallery", verbose_name='Property')
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, verbose_name='Type')
    media_file = models.FileField(upload_to='property_gallery/', verbose_name='Media File')

    def __str__(self):
        return f'{self.property.title} - {self.type}'
    

class News(models.Model):
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True, default="thumbnails/default-news.jpeg")
    title = models.CharField(max_length=255, verbose_name='Title')
    subtitle = models.CharField(max_length=255, verbose_name='Subtitle')
    description = QuillField(verbose_name='Description')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ("-created_at",)
