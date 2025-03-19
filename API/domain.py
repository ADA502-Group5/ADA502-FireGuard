from pydantic import BaseModel
from typing import Optional

class Registration(BaseModel):
    location_name: str | None = None
    contact_details: str 
    id: Optional[int] = None


class Location(BaseModel):
    location_name: str 
    latitude: float 
    longitude: float
    registrations: list[Registration] = []
