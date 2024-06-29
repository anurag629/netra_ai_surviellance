from pydantic import BaseModel
from datetime import datetime
from typing import List

# Camera Schemas
class CameraBase(BaseModel):
    name: str
    url: str

class CameraCreate(CameraBase):
    pass

class Camera(CameraBase):
    id: int

    class Config:
        orm_mode = True
        

# Log Schemas
class LogBase(BaseModel):
    message: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Person Schemas
class PersonBase(BaseModel):
    name: str
    age: int
    city: str
    country: str
    dob: datetime

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int

    class Config:
        orm_mode = True


class LocationBase(BaseModel):
    latitude: str
    longitude: str
    address: str

class LocationCreate(LocationBase):
    person_id: int

class Location(LocationBase):
    id: int
    person_id: int
    timestamp: datetime
    screenshot: str

    class Config:
        orm_mode = True