from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from .models import OffPlansProperty, OpenHouse, News, ContactForm
from .serializers import *
from .filters import OffPlansPropertyFilter, NewsFilter
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
import requests


def index(request):
    return HttpResponse("<h1>APIs are running</h1>")


class OffPlansPropertyListAPIView(generics.ListAPIView):
    queryset = OffPlansProperty.objects.all()
    serializer_class = OffPlansPropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OffPlansPropertyFilter
    search_fields = ['title', 'developer']
    ordering_fields = ['min_price', 'max_price', 'handover_date']


class OffPlansPropertyDetailAPIView(RetrieveAPIView):
    serializer_class = OffPlansPropertyDetailSerializer
    queryset = OffPlansProperty.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)



class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NewsFilter
    search_fields = ['title', 'subtitle']
    ordering_fields = ['created_at']


class PopularAreaListView(generics.ListAPIView):
    queryset = PopularArea.objects.all()
    serializer_class = PopularAreaSerializer


class AgentProfileListView(generics.ListAPIView):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentProfileSerializer


class NewsDetailAPIView(RetrieveAPIView):
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()


class ContactFormCreateView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer

    def delete(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")
    
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")
    

class OpenHouseListView(generics.ListCreateAPIView):
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer


class XMLAPIView(APIView):

    def get(self, request, format=None):
        # Make the API request and get the XML response
        api_url = 'https://expert.propertyfinder.ae/feed/trinity/propertyfinder/80a211e68bcee54978fb26e4ccd6a9f3?offering_type=RS'
        api_response = requests.get(api_url)
        xml_data = api_response.text

        # Convert the XML response to JSON
        json_data = xmltodict.parse(xml_data)

        return Response(json_data)