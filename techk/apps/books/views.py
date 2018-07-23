from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.books.models import Book
from apps.books.models import BookCategory


class BaseListView(ListView):
    paginate_by = 20

    def paginate_queryset(self, queryset, page_size):
        paginator, page, page_object_list, page_has_other_pages = (
            super(BaseListView, self).paginate_queryset(queryset, page_size)
        )

        paginator.trimmed_page_range = range(
            max(page.number - 5, 1),
            min(page.number + 5, paginator.num_pages + 1)
        )

        return (paginator, page, page_object_list, page_has_other_pages)


class BookList(BaseListView):
    model = Book
    template_name = 'book/list.pug'
    paginate_by = 20


class BookDetail(DetailView):
    model = Book
    template_name = 'book/detail.pug'
    pk_url_kwarg = 'book_id'


class BooksByCategoryList(BaseListView):
    model = Book
    template_name = 'book/list_by_category.pug'
    paginate_by = 20

    def get_queryset(self):
        return Book.objects.filter(
            category_id=self.kwargs.get('category_id')
        )

    def get_context_data(self, **kwargs):
        print("1")
        context = super(
            BooksByCategoryList,
            self
        ).get_context_data(**kwargs)

        print("1")
        category = get_object_or_404(
            BookCategory,
            pk=self.kwargs.get('category_id'),
        )
        print("1")

        context['title'] = category.name

        return context


class BookCategoryList(BaseListView):
    model = BookCategory
    template_name = 'category/list.pug'
