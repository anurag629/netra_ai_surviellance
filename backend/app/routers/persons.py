from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.dependencies import get_db
from app.services.face_recognition_service import save_person_image

router = APIRouter(
    prefix="/persons",
    tags=["persons"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.create_person(db=db, person=person)
    return db_person

@router.post("/{person_id}/upload_image")
def upload_person_image(person_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    save_person_image(person_id, file)
    return {"message": "Image uploaded successfully"}


@router.get("/", response_model=list[schemas.Person])
def read_persons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    return persons


@router.delete("/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    crud.delete_person(db, person_id=person_id)
    return {"message": "Person deleted successfully"}

