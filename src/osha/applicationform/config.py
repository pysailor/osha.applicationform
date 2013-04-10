# -*- coding: utf-8 -*-
"""Global constants."""

from os import getcwd


PROJECTNAME = 'osha.applicationform'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'PFGSaveDataAdapterWithFileUpload': 'PloneFormGen: Add Content',
}

# used to identify file in the results row
PFG_FILE_UPLOAD_PREFIX = 'pfg_file_upload-'

# rdb settings
DB_URL = getcwd() + '/var/osha_applicationform.sqlite'
DB_TYPE = 'sqlite'
JOB_VACANCY_ID = 'job_vacancy'
