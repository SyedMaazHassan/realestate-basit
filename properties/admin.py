from django.contrib import admin
from .models import *
from django.utils.html import format_html

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
    list_display = ['title', 'type', 'location', 'datetime', 'image']

    
@admin.register(PopularArea)
class PopularAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']

    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_type', 'fromm', 'name', 'email', 'phone', 'phone']


class DataUpdateAdmin(admin.ModelAdmin):
    list_display = ['update_id', 'display_machine_info', 'happened_at']

    def display_machine_info(self, obj):
        # Retrieve the associated MachineInfo instance
        machine_info = MachineInfo.objects.get(id=obj.source.id)

        # Create a formatted HTML string with all attributes and line breaks
        machine_info_summary = format_html(
            '''<b>User:</b> {user_name}, 
               <br><b>Host:</b> {hostname}, 
               <br><b>IP:</b> {ip_address}, 
               <br><b>MAC:</b> {mac_address}, 
               <br><b>System:</b> {system}, 
               <br><b>Node Name:</b> {node_name}, 
               <br><b>Release:</b> {release}, 
               <br><b>Machine:</b> {machine}, 
               <br><b>Processor:</b> {processor}''',
            user_name=machine_info.user_name,
            hostname=machine_info.hostname,
            ip_address=machine_info.ip_address,
            mac_address=machine_info.mac_address,
            system=machine_info.system,
            node_name=machine_info.node_name,
            release=machine_info.release,
            machine=machine_info.machine,
            processor=machine_info.processor
        )

        return machine_info_summary

    display_machine_info.short_description = 'Source'  # Column header name


admin.site.register(HomePageSites)
admin.site.register(APIKey)
admin.site.register(News)
admin.site.register(PaymentPlan)
admin.site.register(DataUpdate, DataUpdateAdmin)
admin.site.register(MachineInfo)