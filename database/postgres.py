from dataclasses import dataclass
import psycopg2

from database import scripts 

@dataclass
class Database:
    dbname: str = 'maindb'
    user: str = 'admin'
    password: str = 'nasud2198vsd2dv'
    host: str = 'localhost'
    port: int = '5432'

    _connection = psycopg2.connect(
        dbname= dbname,
        user=user,
        password=password,
        host=host
        )
    
    _cur = _connection.cursor()

    def check_registration(self, username: str = None) -> bool:
        self._cur.execute(scripts.check_registration_script.format(telegram_username=username))
        result = self._cur.fetchone()
        if result:
            return True
        return False
    
    def register_new_user(self, telegram_username: str = None, name_surname: str = None, study_group: str = None)-> None:
        self._cur.execute(scripts.registration_insert_script.format(
            telegram_username=telegram_username,
            name_surname=name_surname,
            study_group=study_group
        ))
        self._connection.commit()
