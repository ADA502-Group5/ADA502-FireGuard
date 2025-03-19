from abc import abstractmethod
import os
from pydantic import BaseModel
from locationreg.domain import Registration
from minio import Minio
from io import BytesIO
from pathlib import Path
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


class RegistrationRepository(AbstractRegistrationRepository):
    """
    using the local file system for persistence
    """

    def __init__(self) -> None:
        self.registrations_dict : dict[int, Registration] = {}
        self.id_counter = 0
        self._read_state()

    def _read_state(self):
        if Path("storage.json").exists():
            fil = open("storage.json", "rt")
            parsed = StoreRegistrations.model_validate_json(fil.read())
            self.registrations_dict = {}
            self.id_counter = len(parsed.registrations)
            for r in parsed.registrations:
                assert r.id is not None
                self.registrations_dict[r.id] = r
            fil.close()

    def _write_current_state(self):
        fil = open("storage.json", "wt")
        storage = []
        for value in self.registrations_dict.values():
            storage.append(value)
        
        fil.write(StoreRegistrations(registrations=storage).model_dump_json())
        fil.close()

    def create_registration(self, contect_details: str, location: str) -> Registration:
        next_id = self.id_counter 
        self.id_counter += 1
        result = Registration(contact_details=contect_details, location_name=location, id=next_id)
        self.registrations_dict[next_id] = result
        self._write_current_state()
        return result

    def read_registrations(self) -> list[Registration]:
        return list(self.registrations_dict.values())
    

    def update_registration(self, reg: Registration):
        assert reg.id is not None and reg.id in self.registrations_dict
        self.registrations_dict[reg.id] = reg
        self._write_current_state()


    def delete_registration(self, reg: Registration):
        assert reg.id is not None and reg.id in self.registrations_dict
        del self.registrations_dict[reg.id]
        self._write_current_state()


class MinioRegistrationRepository(AbstractRegistrationRepository):


    def __init__(self) -> None:
        self.client = Minio(
            endpoint=os.environ["OBJECT_STORAGE_URL"],
            access_key=os.environ["OBJECT_STORAGE_ACCESS_KEY"],
            secret_key=os.environ["OBJECT_STORAGE_SECRET_KEY"],
            secure=False
        )
        self.bucket_name = os.environ["OBJECT_STORAGE_BUCKET"]
        self.registrations_dict : dict[int, Registration] = {}
        self.id_counter = 0
        self._read_state()

    def _read_state(self):
        found = False
        for o in self.client.list_objects(self.bucket_name):
            if o.object_name == "storage.json":
                found = True 
                break
        if not found:
            return
        response = self.client.get_object(self.bucket_name, "storage.json")
        if response.status == 200:
            parsed =  StoreRegistrations.model_validate_json(response.read().decode())
            self.registrations_dict = {}
            self.id_counter = len(parsed.registrations)
            for r in parsed.registrations:
                assert r.id is not None
                self.registrations_dict[r.id] = r
        response.close()

    def _write_current_state(self):
        storage = []
        for value in self.registrations_dict.values():
            storage.append(value)
        
        content = StoreRegistrations(registrations=storage).model_dump_json().encode()
        self.client.put_object(self.bucket_name, "storage.json", BytesIO(content), len(content))

    def create_registration(self, contect_details: str, location: str) -> Registration:
        next_id = self.id_counter 
        self.id_counter += 1
        result = Registration(contact_details=contect_details, location_name=location, id=next_id)
        self.registrations_dict[next_id] = result
        self._write_current_state()
        return result

    def read_registrations(self) -> list[Registration]:
        return list(self.registrations_dict.values())
    

    def update_registration(self, reg: Registration):
        assert reg.id is not None and reg.id in self.registrations_dict
        self.registrations_dict[reg.id] = reg
        self._write_current_state()


    def delete_registration(self, reg: Registration):
        assert reg.id is not None and reg.id in self.registrations_dict
        del self.registrations_dict[reg.id]
        self._write_current_state()



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







