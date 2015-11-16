# -*- coding: utf-8 -*-

import unittest2 as unittest
from plone.app.multilingual.interfaces import ILanguage
from ruddocom.policy.testing import RUDDOCOM_POLICY_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = RUDDOCOM_POLICY_INTEGRATION_TESTING

    def test_portal_title(self):
        portal = self.layer['portal']
        self.assertEqual(
                         "Rudd-O.com",
                         portal.getProperty('title')
                         )

    def test_portal_description(self):
        portal = self.layer['portal']
        self.assertEqual(
                         "Linux, free software, voluntaryism and cypherpunk "
                         "discussion.  Established 1999.",
                         portal.getProperty('description')
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

    def test_ckeditor_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('collective.ckeditor'))

    def test_plonefinder_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('collective.plonefinder'))

    def test_linguaplone_not_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertFalse(qi.isProductInstalled('LinguaPlone'))

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
        l = portal['portal_languages']
        self.assertEquals(l.supported_langs, ['en', 'es'])
        self.assertEquals(l.use_cctld_negotiation, False)
        self.assertEquals(l.use_combined_language_codes, False)
        self.assertEquals(l.use_content_negotiation, True)
        self.assertEquals(l.use_cookie_negotiation, False)
        self.assertEquals(l.use_path_negotiation, False)
        self.assertEquals(l.use_request_negotiation, False)
        self.assertEquals(l.use_subdomain_negotiation, True)

    def test_portal_properties(self):
        portal = self.layer['portal']
        l = portal['portal_properties']['site_properties']
        self.assertEquals(l.default_language, 'en')
        self.assertEquals(l.default_charset, 'utf-8')
        self.assertEquals(l.default_editor, 'CKeditor')
        self.assertEquals(l.visible_ids, True)
        self.assertEquals(l.exposeDCMetaTags, True)
        self.assertEquals(l.default_contenttype, 'text/html')
        self.assertEquals(l.enable_sitemap, True)
        self.assertNotIn("text/x-web-markdown", l.forbidden_contenttypes)
        self.assertIn("<script type=\"text/javascript\">",
                      l.webstats_js)

    def test_safe_html(self):
        portal = self.layer['portal']
        l = portal['portal_transforms']['safe_html']

        permit = ["embed", "object", "style", "iframe"]
        tconfig = l._config
        for p in permit:
            self.assertIn(p, tconfig['valid_tags'])
            self.assertNotIn(p, tconfig['nasty_tags'])

    def test_portal_structure(self):
        site = self.layer['portal']
        l = site['en']
        self.assertEquals(l.title, u'Rudd-O.com in English')
        self.assertEquals(ILanguage(l).get_language(), 'en')
        l = site['es']
        self.assertEquals(l.title, u'Rudd-O.com en español')
        self.assertEquals(ILanguage(l).get_language(), 'es')

    def test_skin_content_appears(self):
        site = self.layer['portal']
        l = site['portal_skins']
        self.assertIn('ruddocom', l)
        s = l['ruddocom']
        self.assertIn('facebook-favicon.png', s)

    def test_cookies(self):
        portal = self.layer['portal']
        l = portal['acl_users']['session']
        self.assertEquals(l.timeout, 604800)
        self.assertEquals(l.cookie_lifetime, 7)
        self.assertEquals(l.secure, True)

    def test_css(self):
        portal = self.layer['portal']
        skins = portal['portal_skins']
        ruddocom = skins["ruddocom"]
        assert "cssoverrides.css" in ruddocom.keys()
        css = portal['portal_css']
        resources = css.resources
        assert "cssoverrides.css" in [ r.getId() for r in resources ]
