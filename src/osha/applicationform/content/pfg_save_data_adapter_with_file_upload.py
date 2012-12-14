# -*- coding: utf-8 -*-
"""Definition of the PFGCorrectAnswersAdapter content type"""

from AccessControl import ClassSecurityInfo
from osha.applicationform.config import PROJECTNAME
from osha.applicationform.interfaces import IPFGSaveDataAdapterWithFileUpload
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
    implements(IPFGSaveDataAdapterWithFileUpload)

    meta_type = "PFGSaveDataAdapterWithFileUpload"
    schema = PFGSaveDataAdapterWithFileUploadSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security.declareProtected(View, 'onSuccess')

    def onSuccess(self, fields, REQUEST=None):
        """The essential method of a PloneFormGen Adapter."""

        import pdb; pdb.set_trace()
        super(PFGSaveDataAdapterWithFileUpload, self).onSuccess(fields, REQUEST)

        print("This is overriden onSucces method")

        # api.content.create()
        # pogledas ce folder "uploads" obstaja in ce ne, kreiras
        # notr v folder kreiras za vsak uploadan file en ATFile
        # aha
        # hm, no bom probal nekaj spacat :)
        # 3. v csv zapises nek ID ki ga dobis iz plone.uuid -> oz. tole more bit prvi korak
        # popravek 2.: v folder uploads nov subfolder z idjem istim kot si ga zapisal v CSV in potem v ta subfolder das ATFile


atapi.registerType(PFGSaveDataAdapterWithFileUpload, PROJECTNAME)
