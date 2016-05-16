from plone import api
from plone.app.testing import PloneSandboxLayer, applyProfile, PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2

class RuddocomPolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ruddocom.policy
        self.loadZCML(package=ruddocom.policy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ruddocom.policy:default')

RUDDOCOM_POLICY_FIXTURE = RuddocomPolicy()
RUDDOCOM_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RUDDOCOM_POLICY_FIXTURE,),
    name="Rudd-O.com:Integration"
)
