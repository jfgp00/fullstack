# -*- coding: utf-8 -*-
#
# standard
from __future__ import unicode_literals

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# utils
from apps.scraper.utils import BookScrapper


class BookCategory(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
    )

    def __str__(self):
        return self.name

    @classmethod
    def scrape_categories(cls):
        scrapper = BookScrapper()
        for category_name in scrapper.scrape_categories():
            cls.objects.get_or_create(
                name=category_name,
            )


class Book(models.Model):
    category = models.ForeignKey(
        'BookCategory',
        verbose_name=_('category'),
        related_name='books',
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
    )
    thumbnail = models.URLField(
        _('thumbnail'),
        null=True,
    )
    price = models.FloatField(
        _('price'),
        null=True,
    )
    stock = models.PositiveIntegerField(
        _('stock'),
        null=True,
    )
    product_description = models.TextField(
        _('product_description'),
        null=True,
    )
    upc = models.CharField(
        _('upc'),
        max_length=255,
        null=True,
    )
    url = models.URLField(
        _('url'),
        null=True,
    )

    def __str__(self):
        if not self.title:
            return 'untitled'
        return self.title

    @classmethod
    def scrape_and_create(cls, with_details=False):
        scrapper = BookScrapper()
        books_urls = scrapper.scrape_book_urls()

        for book_url in books_urls:
            book, created = cls.objects.get_or_create(
                url=book_url,
            )
            if with_details:
                book.scrape_and_update()

    @classmethod
    def scrape_and_update_details(cls, limit=None):
        book_queryset = cls.objects.all()
        scrapper = BookScrapper()

        if limit:
            book_queryset[:limit]

        for book in book_queryset:
            if not book.url:
                continue

            scrapper.scrape_book_details(book)

    def scrape_and_update(self):
        scrapper = BookScrapper()
        return scrapper.scrape_book_details()
