from django.shortcuts import render
from apps.books.models import Book


def index(request):
    context = {}
    context['book_exists'] = Book.objects.exists()
    return render(request, 'index.pug', context)
