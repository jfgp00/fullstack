from apps.books import views
from django.conf.urls import url

urlpatterns = [
    url(
        r'^$',
        views.BookList.as_view(),
        name='book_list',
    ),
]
