from rest_framework import serializers
from .models import News, OffPlansProperty, Location, Gallery, Amenity, ContactForm
from django_quill.forms import QuillFormField



class OffPlansPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = OffPlansProperty
        fields = ['id', 'thumbnail', 'title', 'subtitle', 'min_price', 'max_price', 'developer', 'project_company_logo', 'handover_date']



class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class OffPlansPropertyDetailSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)
    gallery = GallerySerializer(many=True)
    location = LocationSerializer()
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