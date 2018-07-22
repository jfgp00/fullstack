# -*- coding: utf-8 -*-
#
# standard
from __future__ import unicode_literals

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BookCategory(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
    )

    def __str__(self):
        return self.name


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
