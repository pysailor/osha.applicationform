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

        # 1. v csv zapises nek ID ki ga dobis iz plone.uuid
        #     to naredis tako, da dolocis nek uuid in ga dodas v fields
        #      potem naj se zadeva shrani ...
        application_uuid = str(uuid.uuid4())  # uuid4 = random UUID

        REQUEST.form['application_uuid'] = application_uuid


        # # TODO: dodaj application_uuid?
        # atapi.StringField('application_uuid',
        #     required = True,
        #     default = uuid.uuid4(),  # uuid4 = random UUID
        # ),

        # TODO: nekje treba shemo dodati .. tole dodatno polje ...
        # fields = [<FGStringField at /Plone/my-form-folder/first-name>]

        # fields[0].fgField.get(REQUEST) ... tako dobis vrednost

        # ocitno treba v seznam polj dodati uuid pa to v request podturiti,
        # da bo notri in se bo shranilo v CSV

        # REQUEST.form.get("fieldName", "default_val_if_missing")



        folder = plone_api.content.get(UID=application_uuid)
        if not folder:
            form_folder = plone_api.content.get(path=REQUEST["PATH_INFO"])  # TODO: this OK?
            folder = plone_api.content.create(
                container=form_folder,
                type="Folder",
                id=application_uuid,
            )

        # notr v folder kreiras za vsak uploadan file en ATFile
        # save CV and motivation letter
        plone_api.content.create(
            container=folder,
            type="File",
            id="CV",
            file=REQUEST.form['cv_file']
            # TODO: file contents ... cv_file
        )

        plone_api.content.create(
            container=folder,
            type="File",
            id="motivation-letter",
            file=REQUEST.form['motivation-letter_file']
        )

        # NOTE: this has to be called *after* we save files, because otherwise
        # uploaded file contents are not available anymore in REQUEST
        super(PFGSaveDataAdapterWithFileUpload, self).onSuccess(fields, REQUEST)

        # popravek 2.: v folder uploads nov subfolder z idjem istim kot si ga zapisal
        # v CSV in potem v ta subfolder das ATFile



        # TODO: on error transaction abort?


atapi.registerType(PFGSaveDataAdapterWithFileUpload, PROJECTNAME)
