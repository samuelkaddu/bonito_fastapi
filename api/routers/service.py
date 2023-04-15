from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api import database, schemas
from api.repository import service

router = APIRouter(
    prefix="/services",
    tags=['Services']
)

get_db = database.get_db

# SERVER_PATH = "public_html/dev.test.bonitohairspot.com"
SERVER_PATH = "public_html"


@router.get('/all', response_model=List[schemas.Service])
def get_all_services(db: Session = Depends(get_db)):
    response = service.get_all(db)
    return JSONResponse(response)


@router.get('/all/active', response_model=List[schemas.Service])
def get_all_services(db: Session = Depends(get_db)):
    response = service.get_all_active(db)
    return JSONResponse(response)


@router.get('/pending', response_model=List[schemas.Service])
def get_pending_services(db: Session = Depends(get_db)):
    response = service.get_pending(db)
    return response
