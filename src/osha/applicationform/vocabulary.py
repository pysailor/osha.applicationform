from plone import api
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import implements


class OshaJobVacanciesVocabulary(object):
    """Vocabulary that provides a list of job vacancies"""
    implements(IContextSourceBinder)

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog(
            portal_type='PublicJobVacancy',
            review_state='published',
            sort_on='effective',
        )
        terms = [
            SimpleTerm(
                value=item.getId,
                token=item.getId,
                title=item.Title
            ) for item in results
        ]
        return SimpleVocabulary(terms)
