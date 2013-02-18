# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from osha.applicationform.tests.base import IntegrationTestCase

from plone import api
import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of osha.applicationform into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if osha.applicationform is installed with
        portal_quickinstaller.
        """
        self.failUnless(
            self.installer.isProductInstalled('osha.applicationform'))

    def test_uninstall(self):
        """Test if osha.applicationform is cleanly uninstalled."""
        self.installer.uninstallProducts(['osha.applicationform'])
        self.failIf(self.installer.isProductInstalled('osha.applicationform'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IOshaApplicationForm is registered."""
        from osha.applicationform.interfaces import IOshaApplicationFormLayer
        from plone.browserlayer import utils
        self.assertIn(IOshaApplicationFormLayer, utils.registered_layers())

    def test_folder_addable(self):
        """Test if Folder type can be created inside a FormFolder."""
        types = api.portal.get_tool('portal_types')
        allowed_types = types.getTypeInfo('FormFolder').allowed_content_types
        self.failUnless('Folder' in allowed_types)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
