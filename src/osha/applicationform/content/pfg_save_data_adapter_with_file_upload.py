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
from types import StringTypes
from zope.interface import implements
from ZPublisher.HTTPRequest import FileUpload

import uuid

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

        # make up a new random uuid, regardless of what might have been sent
        submission_uuid = str(uuid.uuid4())  # uuid4 = random UUID
        REQUEST.form['submission_uuid'] = submission_uuid

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
        file_folder = plone_api.content.create(
            container=uploads_folder,
            type="Folder",
            id=submission_uuid,
        )

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
                    data.append(
                        '%s-%s' % (PFG_FILE_UPLOAD_PREFIX, submission_uuid))
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

    def get_csv(self):
        """Return saved data in csv format."""

        if getattr(self, 'UseColumnNames', False):
            delimiter = self.csvDelimiter()
            res = "%s\n" % delimiter.join(self.getColumnNames())
            if isinstance(res, unicode):
                res = res.encode(self.getCharset())
        else:
            res = ''

        return '%s%s' % (res, self.getSavedFormInputForEdit())


atapi.registerType(PFGSaveDataAdapterWithFileUpload, PROJECTNAME)
