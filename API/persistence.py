from abc import abstractmethod
import os
from psycopg2 import  connect
from dotenv import load_dotenv
from frcm.datamodel.model import Location
from DataHelper import User


class PgRegistrationRepository():

    load_dotenv()
    def __init__(self) -> None:
        db_host = os.getenv("PG_HOST")
        db_name = os.getenv("PG_NAME")
        db_user = os.getenv("PG_USER")
        db_pass = os.getenv("PG_PASS")
        self.db_prefix = os.getenv("DatabasePrefix")
        self.connection = connect(f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}")
        super().__init__()

    def getLocation(self, name) -> Location:
       
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.db_prefix}.locations WHERE name = %s;"
        
        cursor.execute(query,(name,))
        result = cursor.fetchone()
        cursor.close()
        return result
 

    def createLocation(self, locationName, latitude, longitude):
      
        cursor = self.connection.cursor()
          
        query = f"""INSERT INTO {self.db_prefix}.locations (name, latiude, longitude) 
                VALUES (%s, %s, %s);"""
      
        cursor.execute(query, (locationName, latitude, longitude))
        self.connection.commit()
        cursor.close()
 

    #TODO add delete and update location?

    #TODO get weather data and save/update it to TTF if existing else create?

    def getTTFForGivenDateAndLocation(self, date, locationName) ->float:
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.db_prefix}.weatherdata WHERE timestamp = %s AND location_name = %s"
        
        cursor.execute(query, (date, locationName))
            
        result = cursor.fetchall() 
        cursor.close()
        return result
      
    
    def saveTTFForGivenDataAndLocation(self, date, location, ttf):
      
        cursor = self.connection.cursor()
            
        query = f"""
        INSERT INTO {self.db_prefix}.weatherdata(location_name, time_to_flashover, timestamp)
        VALUES (%s, %s, %s) RETURNING id;
        """
        
        cursor.execute(query, (location, ttf, date))
        inserted_id = cursor.fetchone()[0]
        self.connection.commit()
            
        return inserted_id
    
    def saveUser(self, user:User):
        cursor = self.connection.cursor()
        query = f"""
                insert into {self.db_prefix}.subscribers (email, username, password_hash, location)
                VALUES (%s,%s,%s,%s)
                """
    
        result = cursor.execute(query,(user.user_email, user.user_name, '1234', user.user_location.city))
        #inseted_id = cursor.fetchone()[0]
        self.connection.commit()
        return "User created"
    
    def getUser(self, user_email:str):

        cursor = self.connection.cursor()
        query = f"""
                select * from {self.db_prefix}.subscribers where email = %s"""
        
        cursor.execute(query, (user_email,))
            
        result = cursor.fetchone() 
        cursor.close()
        return result
