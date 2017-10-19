# -*- coding: utf-8 -*-
"""Testing support."""
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.selectivelogin


class SelectiveLoginLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.selectivelogin)

    def setUpPloneSite(self, portal):  # noqa
        """Setup the Plone site."""
        self.applyProfile(portal, 'collective.selectivelogin:default')


SELECTIVELOGIN_FIXTURE = SelectiveLoginLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(SELECTIVELOGIN_FIXTURE,),
    name='SelectiveLoginLayer:IntegrationTesting'
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SELECTIVELOGIN_FIXTURE,),
    name='SelectiveLoginLayer:FunctionalTesting'
)


ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SELECTIVELOGIN_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='SelectiveLoginLayer:AcceptanceTesting'
)
