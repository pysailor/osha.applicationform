# -*- coding: utf-8 -*-
"""Definition of the PFGCorrectAnswersAdapter content type"""

from AccessControl import ClassSecurityInfo
from osha.applicationform.config import PROJECTNAME
from osha.applicationform.interfaces import ISaveDataAdapterWithFileUpload
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View
from Products.PloneFormGen.content.saveDataAdapter import FormSaveDataAdapter
from zope.interface import implements


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
    implements(ISaveDataAdapterWithFileUpload)

    meta_type = "PFGSaveDataAdapterWithFileUpload"
    schema = PFGSaveDataAdapterWithFileUploadSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security.declareProtected(View, 'onSuccess')

    def onSuccess(self, fields, REQUEST=None):
        """The essential method of a PloneFormGen Adapter."""

        super(PFGSaveDataAdapterWithFileUpload, self).onSuccess(fields, REQUEST)

        print("This is overriden onSucces method")


atapi.registerType(PFGSaveDataAdapterWithFileUpload, PROJECTNAME)
