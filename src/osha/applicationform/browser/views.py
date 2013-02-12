from datetime import datetime
from DateTime import DateTime
from osha.applicationform.config import NATIONALITIES
from osha.applicationform.config import PFG_FILE_UPLOAD_PREFIX
from plone.i18n.locales.countries import countries
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


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

    def get_file_url(self, file_id):
        """ Return url to the uploaded file. We need the file prefix to
        identify the file in the results row.
        """
        return "%s/%s/application/view" % (
            self.context.getParentNode()['uploads'].absolute_url(),
            file_id.strip(PFG_FILE_UPLOAD_PREFIX + '-')
        )
