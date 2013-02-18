# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.PloneFormGen.interfaces.actionAdapter import \
    IPloneFormGenActionAdapter
from zope.interface import Interface


class IPFGSaveDataAdapterWithFileUpload(IPloneFormGenActionAdapter):
    """Save form data along with uploaded files."""


class IOshaApplicationFormLayer(Interface):
    """Marker interface for defining a Zope 3 browser layer."""
