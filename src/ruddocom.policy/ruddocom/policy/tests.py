#ila -*- coding: utf-8 -*-

import unittest
import plone.api
from ruddocom.policy.testing import RUDDOCOM_POLICY_INTEGRATION_TESTING
from Products.CMFPlone.interfaces import ILanguageSchema
from Products.CMFPlone.interfaces import ISiteSchema
from zope.component.hooks import setSite
from plone import api


class TestSetup(unittest.TestCase):

    layer = RUDDOCOM_POLICY_INTEGRATION_TESTING

    def test_portal_title(self):
        portal = self.layer['portal']
        self.assertEqual(
                         "Rudd-O.com",
                         portal.getProperty('title')
                         )

    def test_portal_email(self):
        portal = self.layer['portal']
        self.assertEqual(
                         "webmaster@rudd-o.com",
                         portal.getProperty('email_from_address')
        )
        self.assertEqual(
                         "Webmaster at Rudd-O.com",
                         portal.getProperty('email_from_name')
        )

    def test_PloneKeywordManager_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('PloneKeywordManager'))

    def test_ploneappcaching_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('plone.app.caching'))

    def test_multilingual_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('plone.app.multilingual'))
        self.assertTrue(qi.isProductInstalled('archetypes.multilingual'))

    def test_diazo_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('plone.app.theming'))

    def test_redirectiontool_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('RedirectionTool'))

    def test_linguaplone_settings_correct(self):
        portal = self.layer['portal']
        setSite(portal)
        def f(x):
            return api.portal.get_registry_record(x)
        self.assertEquals(f('plone.available_languages'), ['en', 'es'])
        self.assertEquals(f('plone.use_cctld_negotiation'), False)
        self.assertEquals(f('plone.use_combined_language_codes'), False)
        self.assertEquals(f('plone.use_content_negotiation'), True)
        self.assertEquals(f('plone.use_cookie_negotiation'), False)
        self.assertEquals(f('plone.use_path_negotiation'), False)
        self.assertEquals(f('plone.use_request_negotiation'), False)
        self.assertEquals(f('plone.use_subdomain_negotiation'), True)

    def test_portal_properties(self):
        portal = self.layer['portal']
        setSite(portal)
        def f(x):
            return api.portal.get_registry_record(x)
        l= registry.forInterface(ISiteSchema, prefix='plone')
        self.assertEquals(l.default_language, 'en')
        self.assertEquals(l.exposeDCMetaTags, True)
        self.assertEquals(l.enable_sitemap, True)
        self.assertIn("<script type=\"text/javascript\">",
                      l.webstats_js)

    def test_portal_structure(self):
        site = self.layer['portal']
        setSite(portal)
        l = site['en']
        self.assertEquals(l.title, u'Rudd-O.com in English')
        self.assertEquals(plone.api.portal.get_current_language(l), 'en')
        l = site['es']
        self.assertEquals(l.title, u'Rudd-O.com en español')
        self.assertEquals(plone.api.portal.get_current_language(l), 'es')

    def test_cookies(self):
        portal = self.layer['portal']
        l = portal['acl_users']['session']
        self.assertEquals(l.timeout, 604800)
        self.assertEquals(l.cookie_lifetime, 7)
        self.assertEquals(l.secure, True)
