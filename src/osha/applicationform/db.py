"""Module that handles relational database connections and mappings."""

from App.config import getConfiguration
from collective.lead import Database
from collective.lead.interfaces import IDatabase
from five import grok


class OshaApplicationFormDB(grok.GlobalUtility, Database):
    grok.name('osha.applicationformdb')
    grok.provides(IDatabase)

    @property
    def _url(self):
        """Return db connection string which we read from the environment."""
        configuration = getConfiguration()
        try:
            url = configuration.product_config['osha.policy']['hr.database']
        except (AttributeError, KeyError):
            raise KeyError('No product config found! Cannot read hr.database '
                  'connection string.')
        return url

    def _setup_tables(self, metadata, tables):
        """XXX: We need to implement this method, because collective.lead
        expects it, but we don't realy need it, since we're working directly
        with the database.
        """
        pass
