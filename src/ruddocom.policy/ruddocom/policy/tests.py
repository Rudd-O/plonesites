import unittest2 as unittest
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

    def test_linguaplone_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('LinguaPlone'))

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
        self.assertEquals(l.force_language_urls, True)
