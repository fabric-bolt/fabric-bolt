from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAccountViews(TestCase):

    def setUp(self):
        password = 'mypassword'

        self.user = User.objects.create_superuser(email='myemail@test.com', password=password, first_name='ted')
        self.user_john = User.objects.create_superuser(email='john@example.com', password=password, first_name='john')

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

    def test_accounts_user_change(self):

        self.assertEqual(User.objects.all().count(), 2)

        view = reverse('accounts_user_delete', args=(self.user_john.pk,))

        post_response = self.client.post(view)

        self.assertTrue(post_response.status_code, 302)

        self.assertEqual(User.objects.all().count(), 1)


    def test_accounts_user_view(self):
        view = reverse('accounts_user_view', args=(self.user_john.pk,))

        get_response = self.client.get(view)

        self.assertTrue(get_response.status_code, 200)

        self.assertTrue('deployment_table' in get_response.context)
        self.assertEqual(len(get_response.context['deployment_table'].data), 0)
