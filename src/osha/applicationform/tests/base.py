# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import unittest2 as unittest


class OshaApplicationformLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import osha.applicationform
        import Products.PublicJobVacancy
        import Products.DataGridField
        import Products.PFGDataGrid
        import Products.RichDocument
        self.loadZCML(package=osha.applicationform)
        self.loadZCML(package=Products.PublicJobVacancy)
        self.loadZCML(package=Products.DataGridField)
        self.loadZCML(package=Products.PFGDataGrid)
        self.loadZCML(package=Products.RichDocument)
        z2.installProduct(app, 'osha.applicationform')
        z2.installProduct(app, 'Products.PublicJobVacancy')
        z2.installProduct(app, 'Products.DataGridField')
        z2.installProduct(app, 'Products.PFGDataGrid')
        z2.installProduct(app, 'Products.PloneFormGen')
        z2.installProduct(app, 'Products.RichDocument')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'osha.applicationform:default')

        # Login and create some test
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')

        # Commit so that the test browser sees these objects
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'osha.applicationform')
        z2.uninstallProduct(app, 'Products.PublicJobVacancy')
        z2.uninstallProduct(app, 'Products.DataGridField')
        z2.uninstallProduct(app, 'Products.PFGDataGrid')
        z2.uninstallProduct(app, 'Products.PloneFormGen')
        z2.uninstallProduct(app, 'Products.RichDocument')


FIXTURE = OshaApplicationformLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="OshaApplicationformLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="OshaApplicationformLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
