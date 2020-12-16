# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from ruddocom.theme.testing import RUDDOCOM_THEME_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that ruddocom.theme is properly installed."""

    layer = RUDDOCOM_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ruddocom.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ruddocom.theme'))

    def test_browserlayer(self):
        """Test that IRuddocomThemeLayer is registered."""
        from ruddocom.theme.interfaces import (
            IRuddocomThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(IRuddocomThemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = RUDDOCOM_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['ruddocom.theme'])

    def test_product_uninstalled(self):
        """Test if ruddocom.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ruddocom.theme'))

    def test_browserlayer_removed(self):
        """Test that IRuddocomThemeLayer is removed."""
        from ruddocom.theme.interfaces import \
            IRuddocomThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(IRuddocomThemeLayer, utils.registered_layers())
