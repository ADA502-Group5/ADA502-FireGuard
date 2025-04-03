from abc import abstractmethod
import os
from pydantic import BaseModel
from DataHelper import Location, Registration
from psycopg2 import  connect
from dotenv import load_dotenv


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

    load_dotenv()
    def __init__(self) -> None:
        db_host = os.getenv("PG_HOST")
        db_name = os.getenv("PG_NAME")
        db_user = os.getenv("PG_USER")
        db_pass = os.getenv("PG_PASS")
        self.connection = connect(f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}")
        super().__init__()

    # def read_registrations(self) -> list[Registration]:
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT id, contact_details, location_name FROM registrations")
    #     result = []
    #     for row in cursor.fetchall():
    #         result.append(Registration(id=row[0], contact_details=row[1], location_name=row[2]))
    #     cursor.close()
    #     return result
    
    def getLocation(self, locationName)-> Location:
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM public.locations WHERE name = '{locationName}'"
        
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            
            cursor.close()
            return result
        except:
          connect.rollback()

    def getTTFForGivenDateAndLocation(self, date, location) ->list[float]:
        cursor = self.connection.cursor()
        query = "SELECT * FROM weatherdata WHERE date = %s AND location = %s"
    
        cursor.execute(query, (date, location))  # Pass parameters as a tuple
        result = []
        for row in cursor.fetchall():
            result.append(row[0])
        cursor.close()
        return result
    
    def saveTTFForGivenDataAndLocation(self,date,location):
        query = "INSERT INTO users (name, age) VALUES (%s, %s) RETURNING id;"
        cursor.execute(query, (name, age))
        user_id = cursor.fetchone()[0]  # Get the inserted record ID
        conn.commit()  # Save changes

    #TODO, make the other CRUD operations





