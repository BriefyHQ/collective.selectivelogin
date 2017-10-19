# -*- coding: utf-8 -*-
from collective.selectivelogin.interfaces import ISelectiveLoginSettings
from collective.selectivelogin.testing import FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter
from zope.component import getUtility

import transaction
import unittest


class LoginFunctionalTest(unittest.TestCase):
    """Test that changes in the selective logincontrol panel are actually stored in the registry."""

    layer = FUNCTIONAL_TESTING

    def _enable(self):
        """Enable selective.login."""
        with transaction.manager:
            api.portal.set_registry_record('enabled', True, interface=ISelectiveLoginSettings)

    def _disable(self):
        """Disable selective.login."""
        with transaction.manager:
            api.portal.set_registry_record('enabled', False, interface=ISelectiveLoginSettings)

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        with transaction.manager:
            api.portal.set_registry_record(
                'allowed_domains', u'plone.com', interface=ISelectiveLoginSettings
            )
            api.portal.set_registry_record(
                'error_message', u'You shall not pass!!!', interface=ISelectiveLoginSettings
            )
            self.user_1 = api.user.create(
                username='bob',
                email='bob@plone.org',
                password='123456'
            )
            self.user_2 = api.user.create(
                username='alice',
                email='alice@plone.com',
                password='123456'
            )

    def test_normal_login(self):
        self._disable()
        self.browser.open("%s/login" % self.portal_url)
        self.browser.getControl(name='__ac_name').value = 'bob'
        self.browser.getControl(name='__ac_password').value = '123456'
        self.browser.getControl(name='submit').click()
        self.assertIn('You are now logged in', self.browser.contents)
        self.browser.open("%s/logout" % self.portal_url)

    def test_invalid_domain(self):
        self._enable()
        self.browser.open("%s/login" % self.portal_url)
        self.browser.getControl(name='__ac_name').value = 'bob'
        self.browser.getControl(name='__ac_password').value = '123456'
        self.browser.getControl(name='submit').click()
        self.assertIn('You shall not pass!!!', self.browser.contents)

    def test_valid_domain(self):
        self._enable()
        self.browser.open("%s/login" % self.portal_url)
        self.browser.getControl(name='__ac_name').value = 'alice'
        self.browser.getControl(name='__ac_password').value = '123456'
        self.browser.getControl(name='submit').click()
        self.assertIn('You are now logged in', self.browser.contents)
        self.browser.open("%s/logout" % self.portal_url)
