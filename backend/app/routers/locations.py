from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    db_location = crud.create_location(db=db, location=location)
    return db_location

@router.get("/", response_model=list[schemas.Location])
def read_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations

@router.get("/person/{person_id}", response_model=list[schemas.Location])
def read_locations_by_person(person_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = crud.get_locations_by_person(db, person_id=person_id, skip=skip, limit=limit)
    return locations
