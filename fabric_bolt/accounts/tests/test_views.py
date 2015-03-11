from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class TestHooks(TestCase):

    def setUp(self):
        password = 'mypassword'

        self.user = User.objects.create_superuser(email='myemail@test.com', password=password, first_name='ted')

        # You'll need to log him in before you can send requests through the client
        self.client.login(email=self.user.email, password=password)

    def test_accounts_user_change(self):

        g = Group.objects.get(name='Admin')

        view = reverse('accounts_user_change', args=(self.user.pk,))

        get_response = self.client.get(view)

        self.assertTrue(get_response.status_code, 200)

        post_response = self.client.post(view, {
            'first_name': 'sue',
            'email': 'myemail@test.com',
            'is_active': True,
            'user_level': g.pk
        })

        u = User.objects.get(pk=self.user.pk)

        self.assertEqual(u.first_name, 'sue')

