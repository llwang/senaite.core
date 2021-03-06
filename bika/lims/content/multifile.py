# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE.rst, CONTRIBUTORS.rst.

from bika.lims import bikaMessageFactory as _
from bika.lims import config
from bika.lims.content.bikaschema import BikaSchema
from bika.lims.interfaces import IMultifile
from plone.app.blob.field import FileField
from Products.Archetypes import atapi
from Products.Archetypes.public import BaseContent
from zope.interface import implements


schema = BikaSchema.copy() + atapi.Schema((

    atapi.StringField(
        "DocumentID",
        required=1,
        searchable=True,
        validators=("uniquefieldvalidator",),
        widget=atapi.StringWidget(
            label=_("Document ID"),
        )
    ),

    FileField(
        "File",
        required=1,
        widget=atapi.FileWidget(
            label=_("Document"),
            description=_("File upload "),
        )
    ),

    atapi.StringField(
        "DocumentVersion",
        widget=atapi.StringWidget(
            label=_("Document Version"),
        )
    ),

    atapi.StringField(
        "DocumentLocation",
        searchable=True,
        widget=atapi.StringWidget(
            label=_("Document Location"),
            description=_("Location where the document set is shelved"),
        )
    ),

    atapi.StringField(
        "DocumentType",
        required=1,
        searchable=True,
        widget=atapi.StringWidget(
            label=_("Document Type"),
            description=_("Type of document (e.g. user manual, instrument "
                          "specifications, image, ...)"),
        )
    ),
))

TitleField = schema['title']
TitleField.required = 0
TitleField.widget.visible = False


class Multifile(BaseContent):
    implements(IMultifile)
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        # ResourceLockedError: Object "multifile..." is locked via WebDAV
        self.wl_clearLocks()
        renameAfterCreation(self)

    def Title(self):
        """Return the DocumentID as Title
        """
        return self.getDocumentID()


atapi.registerType(Multifile, config.PROJECTNAME)
