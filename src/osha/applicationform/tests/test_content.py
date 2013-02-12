# -*- coding: utf-8 -*-
"""Tests for osha.applicationform content types."""

from osha.applicationform.tests.base import IntegrationTestCase

from plone import api
import unittest2 as unittest


class TestPFGSaveDataAdapterWithFileUpload(IntegrationTestCase):
    """Test PFGSaveDataAdapterWithFileUpload type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self._create_test_content()

    def _create_test_content(self):
        """Create some content, needed for testing."""

        # first create a PFG form folder
        self.form = api.content.create(
            container=self.portal,
            type="FormFolder",
            title="Form Foo"
        )

        # create a few fields
        self.name = api.content.create(
            container=self.form,
            type="FormStringField",
            title="Name"
        )
        self.surname = api.content.create(
            container=self.form,
            type="FormStringField",
            title="Surname"
        )
        self.application = api.content.create(
            container=self.form,
            type="FormFileField",
            title="Application"
        )

        # create a save data adapter with file upload
        self.adapter = api.content.create(
            container=self.portal['form-foo'],
            type="PFGSaveDataAdapterWithFileUpload",
            title="Save adapter with upload"
        )

    def test_on_success_upload_folder_created(self):
        """Test onSuccess method if the upload folder is created."""
        fields = [self.name, self.surname]
        self.adapter.onSuccess(fields, self.layer['request'])

        # there should be a folder for uploads and a folder for file
        # submissions (it has a random uuid so we just check that an
        # item is there)
        self.assertIn('uploads', self.form.keys())
        self.assertEqual(len(self.form['uploads'].keys()), 1)

    def test_on_success_nofile(self):
        """Test onSuccess method if there are no file fields."""
        fields = [self.name, self.surname]
        self.layer['request'].form = {
            'name': 'johnny',
            'surname': 'bravo'
        }

        self.adapter.onSuccess(fields, self.layer['request'])
        results = [it for it in self.adapter.getSavedFormInput()]
        self.assertEqual(results, [['johnny', 'bravo']])

    def test_on_success_file_upload(self):
        """Test onSuccess method if there is a file field."""
        fields = [self.name, self.surname, self.application]
        self.layer['request'].form = {
            'name': 'johnny',
            'surname': 'bravo',
            #'application_file': should be a
            #    ZPublisher.HTTPRequest.FileUpload instance
        }

        self.adapter.onSuccess(fields, self.layer['request'])
        results = [it for it in self.adapter.getSavedFormInput()]

        # XXX: currently we just test that results are not None, because
        # we need to figure out how to test file upload
        self.assertIsNotNone(results)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
