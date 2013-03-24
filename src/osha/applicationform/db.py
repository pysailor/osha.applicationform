"""Module that handles relational database connections and mappings."""

from collective.lead import Database
from collective.lead.interfaces import IDatabase
from five import grok
from osha.applicationform.config import DB_TYPE
from osha.applicationform.config import DB_URL

import sqlalchemy as sa


class OshaApplicationFormDB(grok.GlobalUtility, Database):
    grok.name('osha.applicationformdb')
    grok.provides(IDatabase)

    @property
    def _url(self):
        return sa.engine.url.URL(drivername=DB_TYPE, database=DB_URL)

    def _setup_tables(self, metadata, tables):
        """XXX: We need to implement this method, because collective.lead
        expects it, but we don't realy need it, since we're working directly
        with the database.
        """
        pass
