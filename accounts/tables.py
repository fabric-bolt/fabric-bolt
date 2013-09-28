"""
Tables for the account app
"""
from django.contrib.auth import get_user_model

import django_tables2 as tables
from django_tables2.utils import A

from core.mixins.tables import ActionsColumn, PaginateTable


class UserListTable(PaginateTable):
    """
    Table for displaying users.
    """

    actions = ActionsColumn([
        #Edit action opens modal
        {'title': 'Edit', 'url': 'accounts_user_change', 'args': [A('pk')]},
        {'title': 'Delete', 'attrs': {'class': 'js-delete'}, 'url': 'accounts_user_delete', 'args': [A('pk')]}
    ])
    email = tables.Column(verbose_name='Email')
    first_name = tables.Column(verbose_name='First Name')
    last_name = tables.Column(verbose_name='Last Name')
    #user_level = tables.Column(verbose_name='User Level', accessor='group_strigify', order_by='groups')  # Bummer, I need a group_strigify method on the user model...

    class Meta:
        model = get_user_model()
        sequence = fields = ('first_name', 'last_name', 'is_active', 'email', )
        attrs = {'class': 'table table-striped table-bordered table-hover'}

    def __init__(self, *args, **kwargs):
        super(UserListTable, self).__init__(*args, **kwargs)

