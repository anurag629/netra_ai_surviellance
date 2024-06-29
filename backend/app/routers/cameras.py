from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db
from app.services.camera_service import generate_frames
from app.services.face_recognition_service import recognize_faces
from app.services.yolo_service import detect_objects_yolo
import face_recognition

router = APIRouter(
    prefix="/cameras",
    tags=["cameras"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Camera)
def create_camera(camera: schemas.CameraCreate, db: Session = Depends(get_db)):
    return crud.create_camera(db=db, camera=camera)

@router.get("/{camera_id}", response_model=schemas.Camera)
def read_camera(camera_id: int, db: Session = Depends(get_db)):
    db_camera = crud.get_camera(db, camera_id=camera_id)
    if db_camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    return db_camera

@router.get("/", response_model=list[schemas.Camera])
def read_cameras(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cameras = crud.get_cameras(db, skip=skip, limit=limit)
    return cameras

@router.get("/{camera_id}/stream_objects")
def stream_camera_objects(camera_id: int, db: Session = Depends(get_db), latitude: str = "", longitude: str = "", address: str = ""):
    db_camera = crud.get_camera(db, camera_id=camera_id)
    if db_camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    db_camera_url = db_camera.url + "/video"
    return StreamingResponse(detect_objects_yolo(db_camera_url, db, latitude=latitude, longitude=longitude, address=address), media_type="multipart/x-mixed-replace; boundary=frame")


@router.delete("/{camera_id}")
def delete_camera(camera_id: int, db: Session = Depends(get_db)):
    db_camera = crud.get_camera(db, camera_id=camera_id)
    if db_camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    crud.delete_camera(db, camera_id=camera_id)
    return {"message": "Camera deleted successfully"}