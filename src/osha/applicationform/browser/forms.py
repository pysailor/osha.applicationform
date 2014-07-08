from osha.applicationform import _
from osha.applicationform.vocabulary import OshaJobVacanciesVocabulary
from plone import api
from z3c.form import button
from z3c.form import form
from z3c.form import field
from zope.interface import Interface
from zope.schema import Set, Choice

import logging

logger = logging.getLogger('osha.applicationform.forms')


class ISendJobVacancyData(Interface):
    vacancies = Set(
        title=_(u"Job vacancies"),
        description=_(u"Select the job vacancies to send"),
        value_type=Choice(source=OshaJobVacanciesVocabulary()),
    )


class SendJobVacancyDataForm(form.Form):
    fields = field.Fields(ISendJobVacancyData)
    ignoreContext = True

    @button.buttonAndHandler(u'Send')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False

        vacancies_list = [i for i in data['vacancies']]
        if not vacancies_list:
            api.portal.show_message(
                message="Please select a list of job vacancies.",
                request=self.request,
                type='error'
            )
            return False

        view = self.context.restrictedTraverse('@@osh-send-data')

        try:
            view.send_data(vacancies=vacancies_list)
            api.portal.show_message(
                message="Applications have been sent for these job "
                "vacancies: {0}".format(', '.join(vacancies_list)),
                request=self.request,
                type='info'
            )
        except:
            logger.exception(
                'Error sending applications for job vacancies: {0} '.format(
                    ','.join(vacancies_list))
            )
            api.portal.show_message(
                message="Error sending applications. Please contact site "
                "administrator.",
                request=self.request,
                type='error'
            )
