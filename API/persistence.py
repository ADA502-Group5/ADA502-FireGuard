from abc import abstractmethod
import os
from pydantic import BaseModel
from DataHelper import Registration
from psycopg2 import  connect


class StoreRegistrations(BaseModel):
    registrations : list[Registration]

class AbstractRegistrationRepository:
    
    @abstractmethod
    def create_registration(self, contect_details: str, location: str) -> Registration:
        pass

    @abstractmethod
    def read_registrations(self) -> list[Registration]:
        pass

    @abstractmethod
    def update_registration(self, reg: Registration):
        pass

    @abstractmethod
    def delete_registration(self, reg: Registration):
        pass

class PgRegistrationRepository(AbstractRegistrationRepository):


    def __init__(self) -> None:
        db_host = os.environ["PG_HOST"]
        db_name = os.environ["PG_NAME"]
        db_user = os.environ["PG_USER"]
        db_pass = os.environ["PG_PASS"]
        self.connection = connect(f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}")
        super().__init__()

    def read_registrations(self) -> list[Registration]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, contact_details, location_name FROM registrations")
        result = []
        for row in cursor.fetchall():
            result.append(Registration(id=row[0], contact_details=row[1], location_name=row[2]))
        cursor.close()
        return result

    #TODO, make the other CRUD operations





