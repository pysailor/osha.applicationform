# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.PloneFormGen.interfaces.actionAdapter import \
    IPloneFormGenActionAdapter


class ISaveDataAdapterWithFileUpload(IPloneFormGenActionAdapter):
    """Save form data along with uploaded files."""
