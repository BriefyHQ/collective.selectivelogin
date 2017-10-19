# -*- coding: utf-8 -*-
from collective.selectivelogin.interfaces import ISelectiveLoginSettings
from collective.selectivelogin.testing import FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class SelectiveLoginFunctionalTest(unittest.TestCase):
    """Test that changes in the selective logincontrol panel are actually stored in the registry."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_selectivelogin_controlpanel_link(self):
        self.browser.open(
            "%s/@@overview-controlpanel" % self.portal_url)
        self.browser.getLink('Selective Login Settings').click()

    def test_selectivelogin_controlpanel_backlink(self):
        self.browser.open(
            "%s/@@selectivelogin-controlpanel" % self.portal_url)
        self.assertTrue("General" in self.browser.contents)

    def test_selectivelogin_controlpanel_sidebar(self):
        self.browser.open(
            "%s/@@selectivelogin-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertTrue(
            self.browser.url.endswith('/plone/@@overview-controlpanel')
        )

    def test_selectivelogin_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="selectivelogin-controlpanel")
        self.assertTrue(view())

    def test_selectivelogin_controlpanel_values(self):
        self.browser.open(
            "%s/@@selectivelogin-controlpanel" % self.portal_url)
        self.browser.getControl(
            name='form.widgets.enabled:list').getControl(value='selected', index=0).selected = True
        self.browser.getControl(
            name='form.widgets.allowed_domains').value = u'plone.org\nplone.com'
        self.browser.getControl(
            name='form.widgets.error_message').value = u'You shall not pass!!!'
        self.browser.getControl(name='form.buttons.save').click()

        enabled = api.portal.get_registry_record('enabled', interface=ISelectiveLoginSettings)
        self.assertTrue(enabled)
        allowed_domains = api.portal.get_registry_record('allowed_domains', interface=ISelectiveLoginSettings)
        self.assertEquals(allowed_domains, u'plone.org\nplone.com')
        error_message = api.portal.get_registry_record('error_message', interface=ISelectiveLoginSettings)
        self.assertEquals(error_message, u'You shall not pass!!!')

