from plone import api
from plone.app.testing import PloneSandboxLayer, applyProfile, PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2
from zope.configuration import xmlconfig
import logging
import sys


class RuddocomPolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ruddocom.policy
        xmlconfig.file(
            'configure.zcml',
            ruddocom.policy,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ruddocom.policy:default')

RUDDOCOM_POLICY_FIXTURE = RuddocomPolicy()
RUDDOCOM_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RUDDOCOM_POLICY_FIXTURE,),
    name="Rudd-O.com:Integration"
)


handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("GenericSetup.ruddocom.policy")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
