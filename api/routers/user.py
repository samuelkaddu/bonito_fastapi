from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api import schemas, database, oauth2
from api.repository import user

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

get_db = database.get_db


@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    # current_user: schemas.User = Depends(oauth2.get_current_user)
    # if not current_user.isAdmin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"User not allowed to perform action")
    response = user.create(request, db)
    if not response:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Success"}


@router.get('/all', status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    # if not current_user.isAdmin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"User not allowed to perform action")
    return user.get_users(db)


@router.put('/update', status_code=status.HTTP_200_OK)
def update_user(request: schemas.User, db: Session = Depends(get_db)):
    user.update(request, db)
    return {'message': 'Success'}


@router.put('/', status_code=status.HTTP_200_OK)
def reset_user(request: schemas.User, db: Session = Depends(get_db)):
    response = user.get_user_by_username(request, db)

    return {'message': response}
