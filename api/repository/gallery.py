import datetime
import uuid

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models, schemas


def get_active_images(db: Session):
    images = db.query(models.Gallery).filter_by(status='Active').all()
    return images


def get_all(db: Session):
    images = db.query(models.Gallery).filter(
        or_(models.Gallery.status == 'Active', models.Gallery.status == 'Inactive')).all()
    return images


def create(request: schemas.Gallery, db: Session):
    new_image_gallery = models.Gallery(
        public_id=str(uuid.uuid4()),
        src=request.src,
        status=request.status,
        section=request.section,
        created_by=request.created_by,
        create_date=datetime.datetime.now().date()
    )
    db.add(new_image_gallery)
    db.commit()
    db.refresh(new_image_gallery)
    return new_image_gallery


def update(request: schemas.Gallery, db: Session):
    image = db.query(models.Gallery).filter(models.Gallery.public_id == request.public_id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(image, key, value)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def delete(public_id: str, db: Session):
    image = models.Gallery.query.filter_by(public_id=public_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
    return {"message": "Image deleted successfully"}


def image_by_id(public_id: str, db: Session):
    image = db.query(models.Gallery).filter_by(public_id=public_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Image with the id {id} is not available")
    return image


def get_pending_images(db: Session):
    images = db.query(models.Gallery).filter_by(status='Submitted').all()
    if not images:
        return []
    return images


def approve_image(request: schemas.Gallery, db: Session):
    image = db.query(models.Gallery).filter_by(public_id=request.public_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(image, key, value)
    image.modified_date = datetime.datetime.now().date()
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def approve_all_images(modified_by: str, db: Session):
    images = db.query(models.Gallery).filter_by(status='Submitted').all()
    for image in images:
        image.status = 'Active'
        image.modified_by = modified_by
        image.modified_date = datetime.datetime.now().date()
    db.commit()
    return {'status': 'Images have been approved'}
