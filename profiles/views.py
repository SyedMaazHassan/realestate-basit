from django.shortcuts import render
from django.http import HttpResponse
from properties.models import Amenity, OffPlansProperty, Location, News
from faker import Faker
from django.db import transaction
from bs4 import BeautifulSoup
from django.utils.html import escape

fake = Faker()

def create_fake_news():
    for _ in range(10):
        news = News(
            title=fake.sentence(),
            subtitle=fake.sentence()
        )
        news.save()


def generate_fake_quill_text():
    fake_html = f"<p>{fake.paragraph()}</p>"

    # Convert the fake HTML string into a BeautifulSoup object
    soup = BeautifulSoup(fake_html, "html.parser")

    # Manipulate the soup object if needed (e.g., add/remove tags, modify content)

    # Convert the soup object back to a string
    modified_html = str(soup)

    return modified_html


@transaction.atomic
def create_properties(num_properties):
    amenities = Amenity.objects.all()
    for i in range(num_properties):
        property_obj = OffPlansProperty.objects.create(
            title=fake.sentence(),
            subtitle=fake.sentence(),
            min_price=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
            max_price=fake.pydecimal(left_digits=6, right_digits=2, positive=True),
            developer=fake.company(),
            project_company_logo='project_company_logos/default.png',
            handover_date=fake.date_between(start_date='+1d', end_date='+1y'),
            youtube_video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        )
        property_obj.description = fake.text()
        property_obj.amenities.set(amenities.order_by('?')[:3])


# Create your views here.
def index(request):

    # create_properties(20)
    create_fake_news()

    return HttpResponse("good")
