from osha.applicationform import _
from osha.applicationform.vocabulary import OshaJobVacanciesVocabulary
from Products.statusmessages.interfaces import IStatusMessage
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
            IStatusMessage(self.request).addStatusMessage(
                "Please select a list of job vacancies.", 'error')
            return False

        view = self.context.restrictedTraverse('@@osh-send-data')

        try:
            view.send_data(vacancies=vacancies_list)
            IStatusMessage(self.request).addStatusMessage(
                "Applications have been sent for these job "
                "vacancies: {0}".format(', '.join(vacancies_list)), 'info'
            )
        except:
            IStatusMessage(self.request).addStatusMessage(
                "Error sending applications. Please contact site "
                "administrator.", 'error')
            logger.exception(
                'Error sending applications for job vacancies: {0} '.format(
                    ','.join(vacancies_list))
            )
