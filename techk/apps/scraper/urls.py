from apps.scraper import views
from django.conf.urls import url

urlpatterns = [
    url(
        r'^$',
        views.scrape_books,
        name='scrape_books',
    ),
]
