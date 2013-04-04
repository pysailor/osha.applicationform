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

COUNTRIES = [
    'Austria',
    'Belgium',
    'Bulgaria',
    'Cyprus',
    'Czech Republic',
    'Denmark',
    'Estonia',
    'Finland',
    'France',
    'Germany',
    'Greece',
    'Hungary',
    'Ireland',
    'Italy',
    'Latvia',
    'Lithuania',
    'Luxembourg',
    'Malta',
    'The Netherlands',
    'Poland',
    'Portugal',
    'Romania',
    'Slovakia',
    'Slovenia',
    'Spain',
    'Sweden',
    'United Kingdom',
    'Iceland',
    'Norway',
    'Liechtenstein',
]

NATIONALITIES = [
    'Austrian',
    'Belgian',
    'British',
    'Bulgarian',
    'Cypriot',
    'Czech',
    'Danish',
    'Dutch',
    'Estonian',
    'Finnish',
    'French',
    'German',
    'Greek',
    'Hungarian',
    'Icelander',
    'Irish',
    'Italian',
    'Latvian',
    'Liechtensteiner',
    'Lithuanian',
    'Luxembourger',
    'Maltese',
    'Norwegian',
    'Polish',
    'Portuguese',
    'Romanian',
    'Slovakian',
    'Slovenian',
    'Spanish',
    'Swedish',
]

DB_URL = getcwd() + '/var/osha_applicationform.sqlite'
DB_TYPE = 'sqlite'

# job vacancy rdb column id
JOB_VACANCY_ID = 'job_vacancy'

OSHA_HR_EMAIL = 'enter email address here'
