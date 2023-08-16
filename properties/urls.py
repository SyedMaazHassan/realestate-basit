from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),

    path('api/localize-data', FetchPropertyList.as_view(), name="localize-data"),

    path('api/fetch-properties/<property_id>', GetSingleProperty.as_view(), name="get-single-property"),

    path('api/fetch-properties', GetPropertiesFromFile.as_view(), name="get-fetch-properties"),

    path('api/fetch-property/<int:property_id>/', GetSingleProperty.as_view(), name="get-single-property"),

    path('api/offplans/', OffPlansPropertyListAPIView.as_view()),

    path('api/offplans/<int:pk>/', OffPlansPropertyDetailAPIView.as_view()),

    path('api/news/', NewsListView.as_view()),
    
    path('api/news/<int:pk>/', NewsDetailAPIView.as_view()),

    path('api/contact-forms', ContactFormCreateView.as_view(), name='contact-forms-create'),

    path('api/open-houses', OpenHouseListView.as_view(), name='open-houses-list'),

    path('api/popular-areas', PopularAreaListView.as_view(), name='popular-area-list'),

    path('api/agent-profiles', AgentProfileListView.as_view(), name='agent-profile-list'),

    path('api/bookings', BookingCreateView.as_view(), name='bookings'),

    path('api/home-sites', HomePageSitesListView.as_view(), name='home-sites'),


]
