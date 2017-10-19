# -*- coding: utf-8 -*-
"""Test helpers."""
from collective.selectivelogin import utils
from collective.selectivelogin.config import PROJECTNAME
from collective.selectivelogin.interfaces import ISelectiveLoginSettings
from collective.selectivelogin.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest2 as unittest


class TestHelpers(unittest.TestCase):
    """Test helpers."""

    layer = INTEGRATION_TESTING

    def _create_users(self, portal):
        """Create users to our tests."""
        self.user_1 = api.user.create(
            username='bob',
            email='bob@plone.org',
        )
        self.user_2 = api.user.create(
            username='alice',
            email='alice@plone.com',
        )
        self.user_3 = api.user.create(
            username='messi',
            email='messi@fcbarcelona.com',
        )

    def _set_enabled(self, value):
        """Set value of ISelectiveLoginSettings.enabled."""
        api.portal.set_registry_record('enabled', value, interface=ISelectiveLoginSettings)

    def _set_allowed_domains(self, value):
        """Set value of ISelectiveLoginSettings.allowed_domains."""
        api.portal.set_registry_record('allowed_domains', value, interface=ISelectiveLoginSettings)

    def _set_error_message(self, value):
        """Set value of ISelectiveLoginSettings.error_message."""
        api.portal.set_registry_record('error_message', value, interface=ISelectiveLoginSettings)

    def setUp(self):
        """Setup testcase."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self._create_users(self.portal)

    def test_is_enabled(self):
        """Test is_enabled."""
        func = utils.is_enabled
        #  By default, False
        self.assertFalse(func())
        #  Change
        self._set_enabled(True)
        self.assertTrue(func())
        #  If we uninstall, should be false as well
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertFalse(func())

    def test_allowed_domains(self):
        """Test allowed_domains."""
        func = utils.allowed_domains
        #  By default, False
        self.assertEquals(func(), [])
        #  Change
        self._set_allowed_domains(u'plone.org\nplone.com')
        self.assertIn('plone.org', func())
        self.assertIn('plone.com', func())
        self.assertNotIn('plone.gov', func())

    def test_get_error_message(self):
        """Test get_error_message."""
        func = utils.get_error_message
        #  By default, u'Invalid Domain'
        self.assertEquals(func(), u'Invalid domain.')
        #  Change
        self._set_error_message(u'You shall not pass!!')
        self.assertEquals(func(), u'You shall not pass!!')

    def test_user_domain(self):
        """Test user_domain."""
        func = utils.user_domain
        self.assertEquals(func(self.user_1), 'plone.org')
        self.assertEquals(func(self.user_2), 'plone.com')
        self.assertEquals(func(self.user_3), 'fcbarcelona.com')

    def test_validate_user_domain(self):
        """Test validate_user_domain."""
        func = utils.validate_user_domain
        #  No allowed_domains set, so all users would be blocked
        self.assertFalse(func(self.user_1))
        self.assertFalse(func(self.user_2))
        self.assertFalse(func(self.user_3))
        # Let's enabled it for plone domains
        self._set_allowed_domains(u'plone.org\nplone.com')
        self.assertTrue(func(self.user_1))
        self.assertTrue(func(self.user_2))
        self.assertFalse(func(self.user_3))
