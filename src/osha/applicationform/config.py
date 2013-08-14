# -*- coding: utf-8 -*-
"""Global constants."""

PROJECTNAME = 'osha.applicationform'

# rdb settings
JOB_VACANCY_ID = 'job_vacancy'

TEST_DB_SQL = """
CREATE TABLE hr_application_form (
    id INTEGER PRIMARY KEY  NOT NULL UNIQUE,
    job_vacancy VARCHAR,
    mr_ms VARCHAR,
    gender VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    date_of_birth DATETIME,
    phone VARCHAR,
    replyto VARCHAR,
    address VARCHAR,
    postal_code VARCHAR,
    town VARCHAR,
    country VARCHAR,
    nationality VARCHAR,
    where_you_found_us VARCHAR
);

CREATE TABLE hr_application_form_application (
    id INTEGER PRIMARY KEY,
    hr_application_form_id INTEGER,
    type VARCHAR,
    data BLOB,
    FOREIGN KEY(hr_application_form_id) REFERENCES hr_application_form(id)
);

CREATE TABLE hr_application_form_languages_grid (
    id INTEGER PRIMARY KEY,
    hr_application_form_id INTEGER,
    language VARCHAR,
    listening VARCHAR,
    reading VARCHAR,
    spoken_interaction VARCHAR,
    spoken_production VARCHAR,
    writing VARCHAR,
    FOREIGN KEY (hr_application_form_id) REFERENCES hr_application_form(id)
);
"""
