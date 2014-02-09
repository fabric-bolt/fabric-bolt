
from django.contrib import messages

from braces.views import GroupRequiredMixin


class MultipleGroupRequiredMixin(GroupRequiredMixin):

    def check_membership(self, group):
        """ Check required group(s) """
        user_groups = self.request.user.groups.values_list("name", flat=True)
        if isinstance(group, (list, tuple)):
            for req_group in group:
                if req_group in user_groups:
                    return True

        is_member = group in user_groups
        if not is_member:
            messages.add_message(self.request, messages.ERROR, 'You do not have sufficient permissions to do that.')

        return is_member