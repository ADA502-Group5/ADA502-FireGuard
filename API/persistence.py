from abc import abstractmethod
import os
from pydantic import BaseModel
from DataHelper import Location, Registration
from psycopg2 import  connect
from dotenv import load_dotenv

class StoreRegistrations(BaseModel):
    registrations : list[Registration]

class PgRegistrationRepository():

    load_dotenv()
    def __init__(self) -> None:
        db_host = os.getenv("PG_HOST")
        db_name = os.getenv("PG_NAME")
        db_user = os.getenv("PG_USER")
        db_pass = os.getenv("PG_PASS")
        self.connection = connect(f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}")
        super().__init__()

    def getLocation(self, name)-> Location:
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM public.locations WHERE name = %s;"
        
            cursor.execute(query,(name,))
            result = cursor.fetchall()
            print(result)
            
            cursor.close()
            return result
        except:
          self.connection.rollback()

        finally:
            if cursor:
                cursor.close()

    def createLocation(self, locationName, latitude, longitude):
      
        cursor = self.connection.cursor()
          
        query = """INSERT INTO locations (name, latiude, longitude) 
                VALUES (%s, %s, %s);"""
      
        cursor.execute(query, (locationName, latitude, longitude))
        self.connection.commit()
        cursor.close()
 

    #TODO add delete and update location?

    #TODO get weather data and save/update it to TTF if existing else create?

    def getTTFForGivenDateAndLocation(self, date, location) ->list[float]:
        #TODO Test this
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM public.weatherdata WHERE date = %s AND location = %s"
        
            cursor.execute(query, (date, location))
            result = []
            for row in cursor.fetchall():
                result.append(row[0])
            cursor.close()
            return result
        except:
           self.connection.rollback()
        finally:
            if cursor:
                cursor.close()
    
    def saveTTFForGivenDataAndLocation(self, date, location, ttf):
        try:
            cursor = self.connection.cursor()
            
            # Modified query to RETURNING the id of the inserted row
            query = """
            INSERT INTO public.weatherdata(location_name, time_to_flashover, timestamp)
            VALUES (%s, %s, %s) RETURNING id;
            """
            
            # Execute query and get the returned id
            cursor.execute(query, (location, ttf, date))
            
            # Fetch the id of the inserted row
            inserted_id = cursor.fetchone()[0]
            
            # Commit the transaction
            self.connection.commit()
            
            return inserted_id

        except Exception as e:
            self.connection.rollback()

        finally:
            if cursor:
                cursor.close()
