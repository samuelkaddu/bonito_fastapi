import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..hashing import Hash


def create(request: schemas.User, db: Session):
    user = models.User(
        public_id=str(uuid.uuid4()),
        username=request.username,
        firstname=request.firstname,
        lastname=request.lastname,
        role=request.role,
        status=request.status,
        email=request.email,
        isApprover=request.isApprover,
        isReceiveMail=request.isReceiveMail,
        created_by=request.created_by,
        password=Hash.bcrypt(request.password),
        isAdmin=request.isAdmin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="user not found")
    return users


def get_user_by_username(request: schemas.User, db: Session):
    user = db.query(models.User).filter_by(username=request.username, status='Active').first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
