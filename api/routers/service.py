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

SERVER_PATH = "public_html/dev.test.bonitohairspot.com"


@router.get('/all', response_model=List[schemas.Service])
def get_all_services(db: Session = Depends(get_db)):
    response = service.get_all(db)
    return JSONResponse(response)
