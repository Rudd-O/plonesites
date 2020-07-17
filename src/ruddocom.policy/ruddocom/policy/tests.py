#ila -*- coding: utf-8 -*-

import unittest
import plone.api
from ruddocom.policy.testing import RUDDOCOM_POLICY_INTEGRATION_TESTING
from Products.CMFPlone.interfaces import ILanguageSchema
from Products.CMFPlone.interfaces import ISiteSchema
from zope.component.hooks import setSite
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class TestSetup(unittest.TestCase):

    layer = RUDDOCOM_POLICY_INTEGRATION_TESTING

    def test_portal_properties(self):
        reg = getUtility(IRegistry)
        for k, v in [
            ("site_title", "Rudd-O.com"),
            ("email_from_address", "webmaster@rudd-o.com"),
            ("email_from_name", "Webmaster at Rudd-O.com"),
        ]:
            self.assertEqual(v, reg[k])

    def test_Products_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        for p in [
            # Keep me in sync with installOldStyleProducts
            "Products.PloneFormGen",
        ]:
            self.assertTrue(qi.isProductInstalled(p),
                            "%s is not installed"%p)

    def test_cookies(self):
        portal = self.layer['portal']
        l = portal['acl_users']['session']
        self.assertEquals(l.timeout, 604800)
        self.assertEquals(l.cookie_lifetime, 7)
        self.assertEquals(l.secure, True)
