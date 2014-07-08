CREATE TABLE hr_application_form (
    id SERIAL PRIMARY KEY,
    job_vacancy VARCHAR,
    gender VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    date_of_birth TIMESTAMP,
    replyto VARCHAR,
    replyto_retype VARCHAR,
    phone VARCHAR,
    address VARCHAR,
    postal_code VARCHAR,
    town VARCHAR,
    country VARCHAR,
    nationality VARCHAR,
    came_from VARCHAR
);

CREATE TABLE hr_application_form_application (
    id SERIAL PRIMARY KEY,
    hr_application_form_id INTEGER,
    type VARCHAR,
    data BYTEA,
    FOREIGN KEY(hr_application_form_id) REFERENCES hr_application_form(id)
);

CREATE TABLE hr_application_form_languages_grid (
    id SERIAL PRIMARY KEY,
    hr_application_form_id INTEGER,
    language VARCHAR,
    listening VARCHAR,
    reading VARCHAR,
    spoken_interaction VARCHAR,
    spoken_production VARCHAR,
    writing VARCHAR,
    FOREIGN KEY (hr_application_form_id) REFERENCES hr_application_form(id)
);
