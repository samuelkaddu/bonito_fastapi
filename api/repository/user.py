import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session, load_only

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
        isAdmin=request.isAdmin,
        resetPassword=request.resetPassword
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    # users = db.query(models.User).all()
    # excluded_columns = [models.User.password]
    # users = db.query(models.User).options(load_only(*[col.name for col in models.User.__table__.columns if col not in excluded_columns]))
    query = db.query(models.User).options(
        load_only(models.User.isAdmin, models.User.email, models.User.lastname, models.User.firstname,
                  models.User.isReceiveMail,
                  models.User.role, models.User.created_by, models.User.username, models.User.public_id,
                  models.User.isApprover, models.User.resetPassword,
                  models.User.status, models.User.username, ))
    users = query.all()
    if not users:
        raise []
    return users


def get_user_by_username(request: schemas.User, db: Session):
    user = db.query(models.User).filter_by(username=request.username, status='Active').first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


def update(request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.public_id == request.public_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
