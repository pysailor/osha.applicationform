# -*- coding: utf-8 -*-
"""Definition of the PFGCorrectAnswersAdapter content type"""

from AccessControl import ClassSecurityInfo
from osha.applicationform.config import PROJECTNAME
from osha.applicationform.interfaces import IPFGSaveDataAdapterWithFileUpload
from plone import api as plone_api
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View
from Products.PloneFormGen.content.saveDataAdapter import FormSaveDataAdapter
from zope.interface import implements
from ZPublisher.HTTPRequest import FileUpload

import uuid

PFGSaveDataAdapterWithFileUploadSchema = FormSaveDataAdapter.schema.copy() + atapi.Schema((
    # -*- Your Archetypes field definitions here ... -*-
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

PFGSaveDataAdapterWithFileUploadSchema['title'].storage = atapi.AnnotationStorage()
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

    def onSuccess(self, fields, REQUEST=None):
        """The essential method of a PloneFormGen Adapter."""

        # make up a new random uuid, regardless of what might have been sent
        submission_uuid = str(uuid.uuid4())  # uuid4 = random UUID
        REQUEST.form['submission_uuid'] = submission_uuid

        super(PFGSaveDataAdapterWithFileUpload, self).onSuccess(fields, REQUEST)

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
        # for storing filed uploaded by this form submission
        file_folder = plone_api.content.create(
            container=uploads_folder,
            type="Folder",
            id=submission_uuid,
        )

        # now store all uploaded files
        for f in fields:
            if not f.isFileField():
                continue

            field_name = f.fgField.getName()
            file_obj = REQUEST.form.get('{0}_file'.format(field_name))

            if isinstance(file_obj, FileUpload) and file_obj.filename != '':
                plone_api.content.create(
                    container=file_folder,
                    type="File",
                    id=field_name,
                    file=file_obj
                )


atapi.registerType(PFGSaveDataAdapterWithFileUpload, PROJECTNAME)
