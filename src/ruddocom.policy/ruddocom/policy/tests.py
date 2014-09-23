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

    def test_PloneKeywordManager_installed(self):
        portal = self.layer['portal']
        qi = getattr(portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('PloneKeywordManager'))
