# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from apps.books.models import Book


def scrape_books(request):
    Book.scrape_and_create(with_details=True)
    return reverse('home')
