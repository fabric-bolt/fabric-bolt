"""
Tests for accounts app
"""
from django.contrib.auth import get_user_model

from django.test import TestCase
from django.contrib.auth.models import Group

from model_mommy import mommy


class ModelsTest(TestCase):
    def test_user_get_groups(self):
        group = mommy.make(Group, name=u'test-group')
        user = mommy.make(get_user_model(), groups=[group])

        self.assertListEqual(user._get_groups(), [u'test-group'])

        # do it again to test the cached version
        self.assertListEqual(user._get_groups(), [u'test-group'])

    def test_user_is_admin(self):
        user = mommy.prepare(get_user_model())

        self.assertFalse(user.user_is_admin())

        user.save()

        self.assertFalse(user.user_is_admin())

        user.groups.add(mommy.make(Group, name='junk-group'))
        delattr(user, '_cached_groups')

        self.assertFalse(user.user_is_admin())

        user.groups.add(Group.objects.get(name='Admin'))
        delattr(user, '_cached_groups')

        self.assertTrue(user.user_is_admin())

    def test_user_is_deployer(self):
        user = mommy.prepare(get_user_model())

        self.assertFalse(user.user_is_deployer())

        user.save()

        self.assertFalse(user.user_is_deployer())

        user.groups.add(mommy.make(Group, name='junk-group'))
        delattr(user, '_cached_groups')

        self.assertFalse(user.user_is_deployer())

        user.groups.add(Group.objects.get(name='Deployer'))
        delattr(user, '_cached_groups')

        self.assertTrue(user.user_is_deployer())

    def test_user_is_historian(self):
        user = mommy.prepare(get_user_model())

        self.assertFalse(user.user_is_historian())

        user.save()

        self.assertFalse(user.user_is_historian())

        user.groups.add(mommy.make(Group, name='junk-group'))
        delattr(user, '_cached_groups')

        self.assertFalse(user.user_is_historian())

        user.groups.add(Group.objects.get(name='Historian'))
        delattr(user, '_cached_groups')

        self.assertTrue(user.user_is_historian())

    def test_user_group_strigify(self):
        user = mommy.make(get_user_model())

        self.assertEqual(user.group_strigify(), '')

        user.groups.add(mommy.make(Group, name='junk-group'))
        delattr(user, '_cached_groups')

        self.assertEqual(user.group_strigify(), 'junk-group')

        user.groups.add(mommy.make(Group, name='New-Admin'))
        delattr(user, '_cached_groups')

        self.assertEqual(user.group_strigify(), 'junk-group/New-Admin')

    def test_user_gravatar(self):
        user = mommy.make(get_user_model(), email='email@example.com')

        self.assertEqual(user.gravatar(30), '//www.gravatar.com/avatar/5658ffccee7f0ebfda2b226238b1eb6e?s=30&d=mm')

    def test_createsuperuser(self):
        user = get_user_model().objects.create_superuser(email='test@test.com', password='password')
        self.assertTrue(user.user_is_admin())
        self.assertFalse(user.user_is_deployer())
        self.assertFalse(user.user_is_historian())

    def test_createuser(self):
        user = get_user_model().objects.create_user(email='test@test.com', password='password')
        self.assertTrue(user.user_is_historian())
        self.assertFalse(user.user_is_deployer())
        self.assertFalse(user.user_is_admin())
