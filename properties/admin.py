from django.contrib import admin
from .models import *

class GalleryInline(admin.TabularInline):
    model = Gallery

class PaymentPlanInline(admin.TabularInline):
    model = PaymentPlan

class LocationInline(admin.StackedInline):
    model = Location

class AmenitiesInline(admin.TabularInline):
    model = OffPlansProperty.amenities.through


@admin.register(OffPlansProperty)
class OffPlansPropertyAdmin(admin.ModelAdmin):
    inlines = [
        GalleryInline,
        PaymentPlanInline,
        LocationInline,
    ]
    list_display = ['title', 'subtitle', 'developer', 'min_price', 'max_price', 'handover_date']
    search_fields = ['title', 'subtitle', 'developer']
    list_filter = ['developer']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['property', 'type', 'media_file']
    list_filter = ['type']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['property', 'address', 'latitude', 'longitude']
    
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['form_name', 'name', 'phone', 'email', 'received_at']

    
@admin.register(OpenHouse)
class OpenHouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'datetime', 'image']

    
@admin.register(PopularArea)
class PopularAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']

    
admin.site.register(APIKey)
admin.site.register(News)
admin.site.register(PaymentPlan)