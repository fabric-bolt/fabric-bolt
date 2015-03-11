"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from fabric_bolt.hosts.models import full_domain_validator, ValidationError, Host


class SimpleTest(TestCase):
    def test_full_domain_validator_wrong(self):

        def validate():
            full_domain_validator('http://www.google.com/')

        self.assertRaises(ValidationError, validate)

    def test_full_domain_validator_too_long(self):

        def validate():
            full_domain_validator('adawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawadawdawdawdawdawaaaaaadawdaw.com')

        self.assertRaises(ValidationError, validate)

    def test_full_domain_validator_label_too_long(self):

        def validate():
            full_domain_validator('example.comcomcomcomcomcomcomcomcomcomcomcomcomcomcomcomcomcomcomcomcomc')

        self.assertRaises(ValidationError, validate)

    def test_full_domain_validator_bad_characters(self):

        def validate():
            full_domain_validator('exa#mple.com')

        self.assertRaises(ValidationError, validate)

    def test_full_domain_validator_no_domain(self):

        ret = full_domain_validator(False)

        self.assertEqual(ret, None)

    def test_full_domain_validator_valid(self):

        full_domain_validator('google.com')

    def test_full_domain_validator_valid(self):

        full_domain_validator('google.com.')

    def test_hook_unicode(self):
        host = Host()
        host.name = '127.0.0.1'
        host.alias = u'code'

        self.assertEqual(unicode(host), u'code')