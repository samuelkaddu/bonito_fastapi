from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from api import models


def get_all(db: Session):
    service_listing = []
    services = db.query(models.Service).filter(
        or_(models.Service.status == 'Active', models.Service.status == 'Inactive')).all()
    for serv in services:
        listing = [{'name': row.name, 'public_id': row.public_id} for row in
                   db.query(models.ServiceListing).filter_by(service_id=serv.public_id).all()]
        service_listing.append(
            {'image_url': serv.image_url,
             'name': serv.name,
             'public_id': serv.public_id,
             'status': serv.status,
             'section': serv.section,
             'service_list': listing
             })
    return service_listing


def get_all_active(db: Session):
    service_listing = []
    services = db.query(models.Service).filter(
        or_(models.Service.status == 'Active')).all()
    for serv in services:
        listing = [{'name': row.name, 'public_id': row.public_id} for row in
                   db.query(models.ServiceListing).filter_by(service_id=serv.public_id).all()]
        service_listing.append(
            {'image_url': serv.image_url,
             'name': serv.name,
             'public_id': serv.public_id,
             'status': serv.status,
             'section': serv.section,
             'service_list': listing
             })
    return service_listing


def get_pending(db: Session):
    service_listing = []
    services = db.query(models.Service).filter_by(status='Submitted').all()
    for serv in services:
        listing = [{'name': row.name, 'public_id': row.public_id} for row in
                   db.query(models.ServiceListing).filter_by(service_id=serv.public_id).all()]
        service_listing.append(
            {'image_url': serv.image_url,
             'name': serv.name,
             'public_id': serv.public_id,
             'status': serv.status,
             'section': serv.section,
             'service_list': listing
             })
    return service_listing
