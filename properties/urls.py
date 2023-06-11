from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('api/offplans/', OffPlansPropertyListAPIView.as_view()),
    path('api/offplans/<int:pk>/', OffPlansPropertyDetailAPIView.as_view()),

    path('api/news/', NewsListView.as_view()),
    path('api/news/<int:pk>/', NewsDetailAPIView.as_view()),

    path('api/contact-forms', ContactFormCreateView.as_view(), name='contact-forms-create'),

]
