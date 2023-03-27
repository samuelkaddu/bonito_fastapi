import json
import os
from typing import List

import paramiko
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api import schemas, database, oauth2
from api.repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User not allowed to perform action")
    return user.create(request, db)


@router.get('/', status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db),
              current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User not allowed to perform action")
    return user.get_users(db)


@router.put('/', status_code=status.HTTP_200_OK)
def update_user(request: schemas.User, db: Session = Depends(get_db)):
    response = user.update(request, db)
    return {'message': response}


@router.put('/', status_code=status.HTTP_200_OK)
def reset_user(request: schemas.User, db: Session = Depends(get_db)):
    response = user.get_user_by_username(request, db)

    return {'message': response}
