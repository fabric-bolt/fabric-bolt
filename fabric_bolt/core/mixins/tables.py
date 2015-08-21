from __future__ import absolute_import, unicode_literals

from django.core.paginator import Paginator
from django.core import urlresolvers
from django.utils.html import mark_safe

import django_tables2 as tables
from django_tables2.tables import Table
from django_tables2.utils import Accessor as A, AttributeDict


class ActionsColumn(tables.Column):
    """
    This column allows you to pass in a list of links that will form an Action Column
    """
    empty_values = ()
    links = None
    delimiter = None

    def __init__(self, links=None, delimiter=' | ', **kwargs):
        super(ActionsColumn, self).__init__(**kwargs)
        self.orderable = False
        self.delimiter = delimiter
        if links is not None:
            self.links = links

    def render(self, value, record, bound_column):
        if not self.links:
            raise NotImplementedError('Links not assigned.')
        if not isinstance(self.links, (list, tuple,dict)):
            raise NotImplementedError('Links must be an iterable.')

        links = []

        for link in self.links:
            title = link['title']
            url = link['url']
            attrs = link['attrs'] if 'attrs' in link else None

            if 'args' in link:
                args = [a.resolve(record) if isinstance(a, A) else a for a in link['args']]
            else:
                args = None

            attrs = AttributeDict(attrs if attrs is not None else self.attrs.get('a', {}))

            try:
                attrs['href'] = urlresolvers.reverse(url, args=args)
            except urlresolvers.NoReverseMatch:
                attrs['href'] = url

            links.append('<a {attrs}>{text}</a>'.format(
                attrs=attrs.as_html(),
                text=mark_safe(title)
            ))

        return mark_safe(self.delimiter.join(links))


class BooleanColumn(tables.BooleanColumn):
    def render(self, value):
        value = bool(value)

        if value:
            html = '<i class="glyphicon glyphicon-ok"></i>'
        else:
            html = '<i class="glyphicon glyphicon-remove"></i>'

        return mark_safe(html)


class PaginateTable(Table):
    """Generic table class that makes use of Django's built in paginate functionality"""

    def __init__(self, *args, **kwargs):
        super(PaginateTable, self).__init__(*args, **kwargs)
        self.template = kwargs.get('template', 'fancy_paged_tables/table.html')

    def paginate(self, klass=Paginator, per_page=None, page=1, *args, **kwargs):
        """
        Paginates the table using a paginator and creates a ``page`` property
        containing information for the current page.

        :type     klass: Paginator class
        :param    klass: a paginator class to paginate the results
        :type  per_page: `int`
        :param per_page: how many records are displayed on each page
        :type      page: `int`
        :param     page: which page should be displayed.

        Extra arguments are passed to the paginator.

        Pagination exceptions (`~django.core.paginator.EmptyPage` and
        `~django.core.paginator.PageNotAnInteger`) may be raised from this
        method and should be handled by the caller.
        """

        self.per_page_options = [25, 50, 100, 200]  # This should probably be a passed in option

        self.per_page = per_page = per_page or self._meta.per_page

        self.paginator = klass(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        # Calc variables for use in displaying first, adjacent, and last page links
        adjacent_pages = 1  # This should probably be a passed in option

        # Starting page (first page between the ellipsis)
        start_page = max(self.page.number - adjacent_pages, 1)
        if start_page <= 3:
            start_page = 1

        # Ending page (last page between the ellipsis)
        end_page = self.page.number + adjacent_pages + 1
        if end_page >= self.paginator.num_pages - 1:
            end_page = self.paginator.num_pages + 1

        # Paging vars used in template
        self.page_numbers = [n for n in range(start_page, end_page) if 0 < n <= self.paginator.num_pages]
        self.show_first = 1 not in self.page_numbers
        self.show_last = self.paginator.num_pages not in self.page_numbers