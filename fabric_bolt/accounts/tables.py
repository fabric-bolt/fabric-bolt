"""
Tables for the account app
"""
from django.contrib.auth import get_user_model

import django_tables2 as tables

from fabric_bolt.core.mixins.tables import ActionsColumn, PaginateTable, BooleanColumn


class UserListTable(PaginateTable):
    """
    Table for displaying users.
    """

    actions = ActionsColumn(
        [
            {
                'title': '<i class="glyphicon glyphicon-pencil"></i>',
                'url': 'accounts_user_change',
                'args': [tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Edit User', 'data-delay': '{ "show": 300, "hide": 0 }'}
            },
            {
                'title': '<i class="glyphicon glyphicon-trash"></i>',
                'url': 'accounts_user_delete',
                'args': [tables.A('pk')],
                'attrs': {'data-toggle': 'tooltip', 'title': 'Delete User', 'data-delay': '{ "show": 300, "hide": 0 }', 'class': 'js-delete'}
            },
        ],
        delimiter='&#160;&#160;&#160;'
    )

    email = tables.LinkColumn('accounts_user_view', args=[tables.A('pk')], verbose_name='Email')
    first_name = tables.Column(verbose_name='First Name')
    last_name = tables.Column(verbose_name='Last Name')
    is_active = BooleanColumn(verbose_name='Active')
    user_level = tables.Column(verbose_name='User Level', accessor='group_strigify', order_by='groups')

    class Meta:
        model = get_user_model()
        sequence = fields = ('email', 'first_name', 'last_name', 'is_active', 'user_level', )
        attrs = {'class': 'table table-striped table-hover'}
