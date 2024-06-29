from sqlalchemy.orm import Session
from app import models, schemas


# Camera CRUD
def get_camera(db: Session, camera_id: int):
    return db.query(models.Camera).filter(models.Camera.id == camera_id).first()

def get_cameras(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Camera).offset(skip).limit(limit).all()

def create_camera(db: Session, camera: schemas.CameraCreate):
    db_camera = models.Camera(name=camera.name, url=camera.url)
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera

def delete_camera(db: Session, camera_id: int):
    db.query(models.Camera).filter(models.Camera.id == camera_id).delete()
    db.commit()
    

# Log CRUD
def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Log).offset(skip).limit(limit).all()

def create_log(db: Session, log: schemas.LogCreate):
    db_log = models.Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def delete_log(db: Session, log_id: int):
    db.query(models.Log).filter(models.Log.id == log_id).delete()
    db.commit()
    

# Person CRUD
def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()


def get_persons(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Person).offset(skip).limit(limit).all()


def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id)
    if db_person:
        db.delete(db_person)
        db.commit()
    return db_person
    
    
# Location CRUD
def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_locations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Location).offset(skip).limit(limit).all()

def get_locations_by_person(db: Session, person_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Location).filter(models.Location.person_id == person_id).offset(skip).limit(limit).all()