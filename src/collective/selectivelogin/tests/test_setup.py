# -*- coding: utf-8 -*-
"""Test collective.selectivelogin setup."""
from collective.selectivelogin.config import PROJECTNAME
from collective.selectivelogin.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest


class TestInstall(unittest.TestCase):
    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Setup testing environment."""
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        """Test if package is installed."""
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        """Test if Interface Layer is present."""
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('ISelectiveLoginLayer', layers)


class TestUninstall(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Setup testing environment."""
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        """Test package is uninstalled."""
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        """Test Interface layer is removed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('ISelectiveLoginLayer', layers)
