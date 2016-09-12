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
            "plone.app.multilingual",
            "Products.PloneKeywordManager",
            "Products.RedirectionTool",
            "Products.PloneFormGen",
        ]:
            self.assertTrue(qi.isProductInstalled(p),
                            "%s is not installed"%p)

    def test_linguaplone_settings_correct(self):
        reg = getUtility(IRegistry)
        def f(x):
            return reg[x]
        self.assertEquals(f('plone.available_languages'), ['en', 'es'])
        self.assertEquals(f('plone.use_cctld_negotiation'), False)
        self.assertEquals(f('plone.use_combined_language_codes'), False)
        self.assertEquals(f('plone.use_content_negotiation'), True)
        self.assertEquals(f('plone.use_cookie_negotiation'), False)
        self.assertEquals(f('plone.use_path_negotiation'), True)
        self.assertEquals(f('plone.use_request_negotiation'), False)
        self.assertEquals(f('plone.use_subdomain_negotiation'), True)

    def test_portal_properties(self):
        portal = self.layer['portal']
        setSite(portal)
        registry = getUtility(IRegistry)
        l = registry.forInterface(ILanguageSchema, prefix='plone')
        self.assertEquals(l.default_language, 'en')
        l = registry.forInterface(ISiteSchema, prefix='plone')
        self.assertEquals(l.exposeDCMetaTags, True)
        self.assertEquals(l.enable_sitemap, True)
        self.assertIn("<script type=\"text/javascript\">",
                      l.webstats_js)

    def test_portal_structure(self):
        portal = self.layer['portal']
        self.assertEquals(portal['en'].title, u'Rudd-O.com in English')
        self.assertEquals(portal['es'].title, u'Rudd-O.com en español')

    def test_cookies(self):
        portal = self.layer['portal']
        l = portal['acl_users']['session']
        self.assertEquals(l.timeout, 604800)
        self.assertEquals(l.cookie_lifetime, 7)
        self.assertEquals(l.secure, True)
