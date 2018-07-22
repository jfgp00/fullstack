# -*- coding: utf-8 -*-

# standard
from __future__ import unicode_literals
from urllib.parse import urljoin
import re
import requests

# utils
from bs4 import BeautifulSoup


class BookScrapper(object):
    BOOKS_TO_SCRAPE_URL = 'http://books.toscrape.com'
    PARSER = 'html.parser'

    def scrape_categories(self):
        response = requests.get(self.BOOKS_TO_SCRAPE_URL)
        soup = BeautifulSoup(response.content, self.PARSER)
        categories_a_tag = soup.aside.ul.ul.find_all('a')
        categories_name_list = []

        for category_a_tag in categories_a_tag:
            raw_text = ''.join(category_a_tag.find_all(text=True))
            category_text = raw_text.strip()
            categories_name_list.append(category_text)

        return categories_name_list

    def scrape_book_urls(self):
        url = self.BOOKS_TO_SCRAPE_URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, self.PARSER)
        next_page = soup.find(class_='next').a['href']
        next_url = urljoin(url, next_page)
        books_urls = []

        while next_page:
            sections = soup.section.find_all(class_='product_pod')
            for section in sections:
                book_relative_url = section.h3.a['href']
                book_url = urljoin(
                    response.url,
                    book_relative_url,
                )
                books_urls.append(book_url)
            try:
                next_page = soup.find(class_='next').a['href']
            except Exception:
                next_page = None

            if next_page:
                next_url = urljoin(
                    response.url,
                    next_page,
                )
                response = requests.get(next_url)
                soup = BeautifulSoup(response.content, self.PARSER)

        return books_urls

    def scrape_book_details(self, book):

        response = requests.get(book.url)
        soup = BeautifulSoup(response.content, self.PARSER)

        book.title = soup.h1.text

        raw_price = soup.find(class_='price_color').text
        book.price = float(re.sub(r'[^0-9.]', '', raw_price))

        raw_thumbnail_url = soup.find(
            class_='item active'
        ).img.get_attribute_list('src')[0]
        book.thumbnail = urljoin(
            self.BOOKS_TO_SCRAPE_URL,
            raw_thumbnail_url
        )

        raw_stock = soup.find(class_="instock availability").text
        book.stock = int(re.findall(r'\d+', raw_stock)[0])

        product_description_tag = soup.find(
            class_='sub-header'
        ).find_next_sibling('p')
        if product_description_tag:
            raw_product_description = product_description_tag.text
            book.product_description = raw_product_description.rstrip(
                '...more'
            ).strip()

        book.upc = soup.th.next_sibling.text

        category_text = soup.ul.find(
            class_='active'
        ).find_previous('li').text.strip()

        from apps.books.models import BookCategory
        category, created = BookCategory.objects.get_or_create(
            name=category_text
        )
        book.category = category

        book.save()

        return book
