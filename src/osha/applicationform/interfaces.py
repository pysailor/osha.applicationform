# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface


class IOshaApplicationFormLayer(Interface):
    """Marker interface for defining a Zope 3 browser layer."""
