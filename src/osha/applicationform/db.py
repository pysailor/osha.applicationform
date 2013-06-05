"""Module that handles relational database connections and mappings."""

from App.config import getConfiguration
from collective.lead import Database
from collective.lead.interfaces import IDatabase
from five import grok
from osha.applicationform.config import TEST_DB_SQL

import logging
import sqlite3
import tempfile

logger = logging.getLogger('osha.applicationform.db')


class OshaApplicationFormDB(grok.GlobalUtility, Database):
    grok.name('osha.applicationformdb')
    grok.provides(IDatabase)

    @property
    def _url(self):
        """Return db connection string which we read from the environment."""
        configuration = getConfiguration()
        try:
            conf = configuration.product_config['osha.applicationform']
            url = conf['hr.database']
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


class TestDB(grok.GlobalUtility, Database):
    """Temp sqlite database that can be used for testing the form."""
    grok.name('osha.applicationform.testdb')
    grok.provides(IDatabase)

    def __init__(self):
        self._db = self._create_tmp_db()
        self._create_tables()
        super(TestDB, self).__init__()

    def _create_tmp_db(self):
        """Create a temp db.

        XXX: We can't use an in-memory database because it gets deleted when
        connection closes.
        """
        try:
            f = tempfile.NamedTemporaryFile()
            f.close()
        except:
            logger.exception('Error creating a tmp database: ')
            return ''
        logger.info('Created a test database: {0}'.format(f.name))
        return f.name

    def _create_tables(self):
        """Create database tables needed to save the form data."""

        # can't create tables if we don't have a database
        if not self._db:
            return
        try:
            conn = sqlite3.connect(self._db)
            cursor = conn.cursor()
            cursor.executescript(TEST_DB_SQL)
            conn.commit()
        except:
            logger.exception(
                'Error creating tables in tmp database {0}'.format(self._db))

    @property
    def _url(self):
        """Return db connection string."""
        return 'sqlite:///{0}'.format(self._db)

    def _setup_tables(self, metadata, tables):
        """XXX: We need to implement this method, because collective.lead
        expects it, but we don't realy need it, since we're working directly
        with the database.
        """
        pass
