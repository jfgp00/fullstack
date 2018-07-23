from apps.books import views
from django.conf.urls import url

urlpatterns = [
    url(
        r'^$',
        views.BookList.as_view(),
        name='book_list',
    ),
    url(
        r'^(?P<book_id>[\d]+)/$',
        views.BookDetail.as_view(),
        name='book_detail',
    ),
    url(
        r'^categories/$',
        views.BookCategoryList.as_view(),
        name='category_list',
    ),
    url(
        r'^categories/(?P<category_id>[\d]+)/$',
        views.BooksByCategoryList.as_view(),
        name='book_by_category_list',
    ),
]
