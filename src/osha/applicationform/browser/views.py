from datetime import datetime
from DateTime import DateTime
from osha.applicationform.config import NATIONALITIES
from osha.applicationform.config import PFG_FILE_UPLOAD_PREFIX
from plone.i18n.locales.countries import countries
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from StringIO import StringIO

import zipfile


class VacanciesView(BrowserView):
    """ Helper view to get the available job vacancies. """

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(
            portal_type='PublicJobVacancy',
            review_state='published',
            sort_on='effective',
        )
        # return job vacancies that are not past deadline
        return [(item.getId, item.Title) for item in results
                if DateTime(datetime.now()) < item.getObject().deadline]


class CountriesView(BrowserView):
    """ Helper view to get a list of countries. """

    def __call__(self):
        return sorted(countries.getCountryListing(), key=lambda x: x[1])


class NationalitiesView(BrowserView):
    """ Helper view to get a list of nationalities. """

    def __call__(self):
        return [(item.lower(), item) for item in NATIONALITIES]


class PFGSaveDataAdapterWithFileUploadView(BrowserView):
    """ View for displaying saved data (with links to uploaded files) and
    option to export the results.

    INFO: Template is a combination of fg_savedata_view_p3.pt and
    fg_savedata_tabview_p3.pt from Products.PloneFormGen.
    """

    def __call__(self):
        return self.index()

    def get_file_url(self, field_name, submission_id):
        """ Return link to the uploaded file.

        :param field_name: name of the field that we want to fetch the file
            url for
        :submission_id: id of the submission
        """
        # We need the file prefix to identify the file in the results row.
        submission_uuid = submission_id.split(PFG_FILE_UPLOAD_PREFIX)[1]

        return "{0}/{1}/{2}/view".format(
            self.context.getParentNode()['uploads'].absolute_url(),
            submission_uuid,
            field_name
        )


class ExportSavedDataWithFiles(BrowserView):
    """ View for exporting saved data and uploaded files. """

    def __call__(self):
        return self.download()

    def download(self):
        """Download the data in a zip package.

        :returns: ZIP file with saved data in excel format and uploaded files
        :rtype: StringIO binary stream
        """

        output = StringIO()
        zf = zipfile.ZipFile(output, mode='w')
        filename = self.context.id
        uploads = self.context.getParentNode()['uploads']

        try:
            # create an xls file
            zf.writestr(
                '{0}.xls'.format(filename), self.context.get_excel_data())

            # add uploaded files
            for folder in uploads.values():
                for upload in folder.values():
                    zf.writestr(
                        'uploads/{0}/{1}'.format(
                            folder.id, upload.getFilename()),
                        upload.data
                    )
        finally:
            zf.close()

        self.context.REQUEST.response.setHeader(
            "Content-Type",
            "application/zip"
        )
        self.context.REQUEST.response.setHeader(
            'Content-Disposition',
            "attachment; filename=%s.zip" % filename
        )
        return output.getvalue()
