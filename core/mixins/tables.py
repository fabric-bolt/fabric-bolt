from __future__ import absolute_import, unicode_literals

from django.core import urlresolvers
from django.utils.html import mark_safe, escape

import django_tables2 as tables
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