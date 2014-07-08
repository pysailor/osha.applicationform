# -*- coding: utf-8 -*-
"""Tests for osha.applicationform views."""

from DateTime import DateTime
from osha.applicationform.tests.base import IntegrationTestCase
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from StringIO import StringIO

import unittest2 as unittest
import zipfile


def _create_test_content(context):
    """Create some content, needed for testing."""

    # first create a PFG form folder
    context.form = api.content.create(
        container=context.portal,
        type="FormFolder",
        title="Form Foo"
    )

    # delete default fields that are created automatically
    for key in context.form.keys():
        del context.form[key]

    # create a few fields
    context.name = api.content.create(
        container=context.form,
        type="FormStringField",
        title="Name"
    )
    context.surname = api.content.create(
        container=context.form,
        type="FormStringField",
        title="Surname"
    )
    context.application = api.content.create(
        container=context.form,
        type="FormFileField",
        title="Application"
    )

    # create a save data adapter with file upload
    context.adapter = api.content.create(
        container=context.portal['form-foo'],
        type="PFGSaveDataAdapterWithFileUpload",
        title="Save adapter with upload"
    )

    # manually set results on the save data adapter
    context.adapter.setSavedFormInput(
        'nikola, tesla, pfg_file_upload-434348181305fi432f\r\n'
        'morga, freeman, pfg_file_upload-124dsu34fghhha3da5')

    # manually create uploads folder
    api.content.create(
        container=context.form,
        type="Folder",
        title="Uploads"
    )


class TestVocabularyViews(IntegrationTestCase):
    """Test various views that serve as vocabularies for the form."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.workflow = api.portal.get_tool('portal_workflow')

    def test_vacancies_view(self):
        """Test if we get the available job vacancies."""
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        # private - this one shouldn't be among results
        api.content.create(
            container=self.portal,
            type="PublicJobVacancy",
            title="Admin",
            deadline=DateTime('2100-01-01')
        )

        # published
        vacancy2 = api.content.create(
            container=self.portal,
            type="PublicJobVacancy",
            title="Programer",
            deadline=DateTime('2100-01-01')
        )
        self.workflow.setDefaultChain('simple_publication_workflow')
        api.content.transition(obj=vacancy2, transition='publish')

        # published, but the deadline has passed - this one shouldn't be
        # among results
        vacancy3 = api.content.create(
            container=self.portal,
            type="PublicJobVacancy",
            title="CTO",
            deadline=DateTime('2012-01-01')
        )
        self.workflow.setDefaultChain('simple_publication_workflow')
        api.content.transition(obj=vacancy3, transition='publish')

        results = self.portal.restrictedTraverse('@@vacancies-helper')()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ('programer', 'Programer'))

    def test_languages_view(self):
        """Test if we get a list of lanugages."""
        results = self.portal.restrictedTraverse('@@languages-helper')()

        # just test that we get the results without error and that the number
        # of results is reasonably large (because the list could change in
        # the future and we don't want to worry about it)
        self.assertTrue(len(results._values) > 100)


class TestPFGSaveDataAdapterWithFileUploadView(IntegrationTestCase):
    """Test the view for save data adapter."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        _create_test_content(self)

    def test_get_file_url_format(self):
        """Check that the url is in right format."""
        view = self.adapter.restrictedTraverse('@@osh-savedata-tabview')
        url = view.get_file_url(
            'application', 'pfg_file_upload-232385sad334das34f')

        self.assertEqual(
            url, 'http://nohost/plone/form-foo/uploads/232385sad334das34f/application/view')


class TestExportSavedDataWithFiles(IntegrationTestCase):
    """Test the view for exporting saved data and uploaded files."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        _create_test_content(self)
        self.view = self.adapter.restrictedTraverse('@@osh-export-data')

    def test_export(self):
        """Test data export."""
        output = self.view()
        zf = zipfile.ZipFile(StringIO(output))

        # we should get a zip file with an excel file inside
        self.assertEqual(
            self.view.request.response['content-type'], "application/zip")
        self.assertTrue("save-adapter-with-upload.zip" in
                        self.view.request.response['content-disposition'])
        self.assertEqual(zf.namelist(), ['save-adapter-with-upload.xls'])


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
