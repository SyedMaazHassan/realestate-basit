from rest_framework import serializers
from .models import *
from profiles.models import SocialProfile, AgentProfile
from django_quill.forms import QuillFormField
import xmltodict
import re


def contains_only_phone_number(string):
    # Define the regular expression pattern for a phone number (only numerical digits, optional '+' sign at the beginning)
    pattern = r'^\+?\d+$'

    # Use re.match() to check if the entire string matches the pattern
    if re.match(pattern, string):
        return True
    else:
        return False



class OpenHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenHouse
        fields = '__all__'


class OffPlansPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = OffPlansProperty
        fields = ['id', 'thumbnail', 'title', 'subtitle', 'category', 'min_price', 'max_price', 'developer', 'project_company_logo', 'handover_date']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        exclude = ('id', 'property',)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class OffPlansPropertyDetailSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)
    gallery = GallerySerializer(many=True)
    location = LocationSerializer()
    payment_plan = PaymentPlanSerializer(many=True)

    # description_html = serializers.SerializerMethodField()
    class Meta:
        model = OffPlansProperty
        fields = '__all__'


    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['description'] = str(instance.description.html)
        return ret
    


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ('description',)


class HomePageSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSites
        fields = "__all__"

class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['description'] = str(instance.description.html)
        return ret
    

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'

    def validate_phone(self, phone):
        # Add your phone number validation logic here
        if not contains_only_phone_number(phone):  # Assuming you have the contains_only_phone_number function from the previous answer
            raise serializers.ValidationError("Invalid phone number. Phone number must contain only numerical digits.")

        return phone


class PopularAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularArea
        fields = '__all__'


class XMLSerializer(serializers.Serializer):
    xml_data = serializers.CharField()

    def to_representation(self, instance):
        xml_data = instance['xml_data']
        json_data = xmltodict.parse(xml_data)
        return json_data


class SocialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialProfile
        fields = ['facebook', 'linkedin', 'twitter']


class AgentProfileSerializer(serializers.ModelSerializer):
    social_profile = SocialProfileSerializer()

    class Meta:
        model = AgentProfile
        fields = ['id', 'name', 'designation', 'email', 'profile_picture', 'social_profile']


# serializers.py

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('booking_type', 'fromm', 'date', 'time', 'name', 'email', 'phone')
    
    def validate_phone(self, phone):
        # Add your phone number validation logic here
        if not contains_only_phone_number(phone):  # Assuming you have the contains_only_phone_number function from the previous answer
            raise serializers.ValidationError("Invalid phone number. Phone number must contain only numerical digits.")

        return phone