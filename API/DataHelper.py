from typing import List, Optional
from pydantic import BaseModel

class Registration(BaseModel):
    id: int
    contact_details: str
    location_name: str

class Location(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    registrations: Optional[List[Registration]] = []

class UserLocation(BaseModel):
    city: str
    country: str

class User(BaseModel):
    user_name: str
    user_email: str
    user_location: UserLocation