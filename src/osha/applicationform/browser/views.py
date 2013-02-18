from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from DateTime import DateTime
from osha.applicationform import _
from osha.applicationform.config import NATIONALITIES
from osha.applicationform.config import PFG_FILE_UPLOAD_PREFIX
from plone import api
from plone.i18n.locales.countries import countries
from plone.i18n.locales.languages import contentlanguages
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.PFGDataGrid.vocabulary import SimpleDynamicVocabulary

import logging

logger = logging.getLogger('osha.applicationform.views')


SEND_DATA_EMAIL_MESSAGE = u"""Hello,

we're sending you a file with saved user submissions. You can also view the
submissions and export them manually online: {0}

Best regards,
{1}
"""


class VacanciesView(BrowserView):
    """Helper view to get the available job vacancies."""

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
    """Helper view to get a list of countries."""

    def __call__(self):
        return sorted(countries.getCountryListing(), key=lambda x: x[1])


class LanguagesView(BrowserView):
    """Helper view to get a list of languages."""

    def __call__(self):
        languages = sorted(
            [lang[1] for lang in contentlanguages.getLanguageListing()])
        return SimpleDynamicVocabulary(languages)


class NationalitiesView(BrowserView):
    """Helper view to get a list of nationalities."""

    def __call__(self):
        return [(item.lower(), item) for item in NATIONALITIES]


class PFGSaveDataAdapterWithFileUploadView(BrowserView):
    """View for displaying saved data (with links to uploaded files) and
    option to export the results.

    INFO: Template is a combination of fg_savedata_view_p3.pt and
    fg_savedata_tabview_p3.pt from Products.PloneFormGen.
    """

    def __call__(self):
        return self.index()

    def get_file_url(self, field_name, submission_id):
        """Return url to the uploaded file.

        :param field_name: name of the field that we want to fetch the file
            url for
        :submission_id: id of the submission
        """

        # We need the file prefix to identify the file in the results row.
        submission_uuid = submission_id.split(PFG_FILE_UPLOAD_PREFIX)[1]
        uploads = self.context.getParentNode().get('uploads', None)

        if uploads:
            return "{0}/{1}/{2}/view".format(
                uploads.absolute_url(), submission_uuid, field_name)
        else:
            return None


class ExportSavedDataWithFiles(BrowserView):
    """View for exporting saved data and uploaded files."""

    def __call__(self):
        """Download the data in a zip package."""
        filename = self.context.id
        self.context.REQUEST.response.setHeader(
            "Content-Type",
            "application/zip"
        )
        self.context.REQUEST.response.setHeader(
            'Content-Disposition',
            "attachment; filename=%s.zip" % filename
        )
        return self.context.get_data_zipped()


class SendSavedDataWithFiles(BrowserView):
    """View for sending saved data and uploaded files via email."""

    def __call__(self):
        """  """
        path = '/'.join(self.context.getParentNode().getPhysicalPath())
        portal = api.portal.get()
        catalog = api.portal.get_tool('portal_catalog')
        site_properties = api.portal.get_tool(
            'portal_properties').site_properties
        email_charset = site_properties.getProperty('email_charset', 'utf-8')
        sender = portal.getProperty('email_from_address', '')
        recipient = catalog(
            portal_type='FormMailerAdapter',
            path={"query": path, "depth": 1}
        )[0].getObject().recipient_email

        # create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = _(u'HR applications data')
        msg['From'] = sender
        msg['To'] = recipient

        text = SEND_DATA_EMAIL_MESSAGE.format(
            self.context.absolute_url(),
            portal.getProperty('title')
        ).encode(email_charset, 'replace')

        # add body text
        body = MIMEText(
            text,
            _subtype='plain',
            _charset=email_charset
        )
        msg.attach(body)

        # add zip file
        attachment = MIMEBase('application', 'zip')
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename=self.context.id + '.zip'
        )
        attachment.set_payload(self.context.get_data_zipped())
        encoders.encode_base64(attachment)
        msg.attach(attachment)

        # send the message
        mailhost = api.portal.get_tool('MailHost')
        mailhost.send(msg.as_string())
        logger.info('PFG data send to {0}'.format(recipient))

        return 'Data sent to {0}'.format(recipient)
