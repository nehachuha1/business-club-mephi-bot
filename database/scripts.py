create_script = '''
    DROP TABLE IF EXISTS mephi.club_registrations;

    CREATE TABLE IF NOT EXISTS mephi.club_registrations (
        id SERIAL PRIMARY KEY,
        telegram_username varchar(32) NOT NULL UNIQUE,
        name_surname varchar(128) NOT NULL,
        study_group varchar(8) NOT NULL,
        is_admin boolean DEFAULT false NOT NULL
    );
'''

registration_insert_script = '''INSERT INTO mephi.club_registrations (telegram_username, name_surname, study_group) 
                            VALUES ('{telegram_username}', '{name_surname}', '{study_group}');'''

check_registration_script = '''SELECT name_surname FROM mephi.club_registrations WHERE telegram_username='{telegram_username}';'''