from datetime import datetime
from DateTime import DateTime
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
