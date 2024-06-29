from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, index=True)

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    dob = Column(DateTime)
    
    
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="locations")
    latitude = Column(String)
    longitude = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    screenshot = Column(String, nullable=False)
    address = Column(String)
    
Person.locations = relationship("Location", order_by=Location.id, back_populates="person")