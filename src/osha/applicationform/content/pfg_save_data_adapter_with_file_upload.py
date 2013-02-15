# -*- coding: utf-8 -*-
"""Definition of the PFGCorrectAnswersAdapter content type"""

from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from osha.applicationform.config import PFG_FILE_UPLOAD_PREFIX
from osha.applicationform.config import PROJECTNAME
from osha.applicationform.interfaces import IPFGSaveDataAdapterWithFileUpload
from plone import api as plone_api
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View
from Products.CMFPlone.utils import safe_hasattr
from Products.PloneFormGen.config import LP_SAVE_TO_CANONICAL
from Products.PloneFormGen.content.saveDataAdapter import FormSaveDataAdapter
from StringIO import StringIO
from types import StringTypes
from xlwt import easyxf
from xlwt import Formula
from xlwt import Workbook
from zope.interface import implements
from ZPublisher.HTTPRequest import FileUpload

import uuid
import zipfile

PFGSaveDataAdapterWithFileUploadSchema = FormSaveDataAdapter.schema.copy() + \
    atapi.Schema((
        # -*- Your Archetypes field definitions here ... -*-
    ))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

PFGSaveDataAdapterWithFileUploadSchema['title'].storage = \
    atapi.AnnotationStorage()
PFGSaveDataAdapterWithFileUploadSchema['description'].storage = \
    atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    PFGSaveDataAdapterWithFileUploadSchema, moveDiscussion=False)


class PFGSaveDataAdapterWithFileUpload(FormSaveDataAdapter):
    """Saves form data along with uploaded files."""
    implements(IPFGSaveDataAdapterWithFileUpload)

    meta_type = "PFGSaveDataAdapterWithFileUpload"
    schema = PFGSaveDataAdapterWithFileUploadSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security.declareProtected(View, 'onSuccess')

    def onSuccess(self, fields, REQUEST=None, loopstop=False):
        """The essential method of a PloneFormGen Adapter. Saves the data."""

        if LP_SAVE_TO_CANONICAL and not loopstop:
            # LinguaPlone functionality:
            # check to see if we're in a translated
            # form folder, but not the canonical version.
            parent = self.aq_parent
            if (
                safe_hasattr(parent, 'isTranslation') and
                parent.isTranslation() and not parent.isCanonical()
            ):
                # look in the canonical version to see if there is
                # a matching (by id) save-data adapter.
                # If so, call its onSuccess method
                cf = parent.getCanonical()
                target = cf.get(self.getId())
                if (
                    target is not None and
                    target.meta_type == 'PFGSaveDataAdapterWithFileUpload'
                ):
                    target.onSuccess(fields, REQUEST, loopstop=True)
                    return

        # create a folder for uploaded files
        file_folder = self._create_submission_folder()
        submission_uuid = file_folder.id
        REQUEST.form['submission_uuid'] = submission_uuid

        data = []
        for f in fields:
            showFields = getattr(self, 'showFields', [])
            if showFields and f.id not in showFields:
                continue

            # store all uploaded files
            if f.isFileField():
                field_name = f.fgField.getName()
                file_obj = REQUEST.form.get('{0}_file'.format(field_name))

                if (
                    isinstance(file_obj, FileUpload) and
                    file_obj.filename != ''
                ):
                    plone_api.content.create(
                        container=file_folder,
                        type="File",
                        id=field_name,
                        file=file_obj
                    )
                    data.append(PFG_FILE_UPLOAD_PREFIX + submission_uuid)
            elif not f.isLabel():
                val = REQUEST.form.get(f.fgField.getName(), '')
                if not type(val) in StringTypes:
                    # Zope has marshalled the field into
                    # something other than a string
                    val = str(val)
                data.append(val)

        if self.ExtraData:
            for f in self.ExtraData:
                if f == 'dt':
                    data.append(str(DateTime()))
                else:
                    data.append(getattr(REQUEST, f, ''))

        self._addDataRow(data)

    def _create_submission_folder(self):
        """Create a folder for this submission that will hold uploaded files.
        """
        # make up a new random uuid, regardless of what might have been sent
        submission_uuid = str(uuid.uuid4())  # uuid4 = random UUID

        # if the uploads folder does not yet exist, it needs to be created
        form_folder = self.getParentNode()
        uploads_folder_name = "uploads"

        uploads_folder = form_folder.get(uploads_folder_name)
        if not uploads_folder:
            uploads_folder = plone_api.content.create(
                container=form_folder,
                type="Folder",
                id=uploads_folder_name,
            )

        # uploaded files have to be stored separately, so create a folder
        # for storing files uploaded by this form submission
        return plone_api.content.create(
            container=uploads_folder,
            type="Folder",
            id=submission_uuid,
        )

    def get_csv_data(self):
        """Return saved data in csv format."""

        if getattr(self, 'UseColumnNames', False):
            delimiter = self.csvDelimiter()
            res = "%s\n" % delimiter.join(self.getColumnNames())
            if isinstance(res, unicode):
                res = res.encode(self.getCharset())
        else:
            res = ''

        return '%s%s' % (res, self.getSavedFormInputForEdit())

    def get_excel_data(self):
        """Return saved data in excel format.

        File columns contain links to uploaded files. File structure of the
        exported excel file and accompanying files should be like this:

        file.xls
        uploads
        |
        |--submission1_id
           |
           |--some_file.txt
           |
           ...
        |
        |---submission2_id
        |
        ...

        :returns: Field data in excel format
        :rtype: Excel Workbook in binary format
        """

        book = Workbook()
        sheet = book.add_sheet('Sheet-{0}'.format(self.id))
        uploads = self.getParentNode()['uploads']
        data = [self.getColumnNames()] + [i for i in self.getSavedFormInput()]

        for rowx, row in enumerate(data):
            for colx, col in enumerate(row):

                # handle file uploads
                if col.startswith(PFG_FILE_UPLOAD_PREFIX):
                    submission_uuid = col.split(PFG_FILE_UPLOAD_PREFIX)[1]

                    # for now we take only the first file in the folder
                    # XXX: make it work also for multiple uploads per
                    # submission
                    upload = uploads[submission_uuid].values()[0]
                    file_path = 'uploads/{0}/{1}'.format(
                        submission_uuid,
                        upload.getFilename()
                    )

                    # add a relative link to the file
                    # XXX: doesn't seem to work in LibreOffice, only Excel
                    col = Formula(
                        'HYPERLINK("{0}";"view file")'.format(file_path))
                    style = easyxf('font: underline single, color blue;')

                    sheet.write(rowx, colx, col, style)
                else:
                    sheet.write(rowx, colx, col)

        return book.get_biff_data()

    def get_data_zipped(self):
        """Return the data in a zip package.

        :returns: ZIP file with saved data in excel format and uploaded files
        :rtype: StringIO binary stream
        """

        output = StringIO()
        zf = zipfile.ZipFile(output, mode='w')
        filename = self.id
        uploads = self.getParentNode()['uploads']

        try:
            # create an xls file
            zf.writestr(
                '{0}.xls'.format(filename), self.get_excel_data())

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

        return output.getvalue()


atapi.registerType(PFGSaveDataAdapterWithFileUpload, PROJECTNAME)
