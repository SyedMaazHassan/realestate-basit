from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from .models import OffPlansProperty
from .serializers import *
from .filters import OffPlansPropertyFilter


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
