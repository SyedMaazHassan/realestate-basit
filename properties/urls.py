from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('api/offplans/', OffPlansPropertyListAPIView.as_view()),
    path('api/offplans/<int:pk>/', OffPlansPropertyDetailAPIView.as_view()),

    path('api/news/', NewsListView.as_view()),
    path('api/news/<int:pk>/', NewsDetailAPIView.as_view()),

    path('api/contact-forms', ContactFormCreateView.as_view(), name='contact-forms-create'),

    path('api/open-houses', OpenHouseListView.as_view(), name='open-houses-list'),

    path('api/fetch-properties', XMLAPIView.as_view(), name='xml_to_json'),

    path('api/popular-areas', PopularAreaListView.as_view(), name='popular-area-list'),

    path('api/agent-profiles', AgentProfileListView.as_view(), name='agent-profile-list'),
    
]
