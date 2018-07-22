from django.views.generic import ListView

from apps.books.models import Book


class BookList(ListView):
    model = Book
    template_name = 'index.pug'
