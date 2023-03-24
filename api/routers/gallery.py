import json
import os
from typing import List

import paramiko
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api import schemas, database
from api.repository import gallery

router = APIRouter(
    prefix="/gallery",
    tags=['Gallery']
)

get_db = database.get_db

SERVER_PATH = "public_html/dev.test.bonitohairspot.com"


@router.get('/active', response_model=List[schemas.Gallery])
def get_all_active_images(db: Session = Depends(get_db)):
    return gallery.get_active_images(db)


@router.get('/all', response_model=List[schemas.Gallery])
def get_all_images(db: Session = Depends(get_db)):
    return gallery.get_all(db)


@router.get('/pending', status_code=status.HTTP_200_OK)
def get_pending_images(db: Session = Depends(get_db)):
    response = gallery.get_pending_images(db)
    return response


@router.get('/{public_id}', status_code=status.HTTP_200_OK)
def get_image_by_id(public_id: str, db: Session = Depends(get_db)):
    response = gallery.image_by_id(public_id, db)
    return response


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_image(request: schemas.Gallery, db: Session = Depends(get_db)):
    return gallery.create(request, db)


@router.put('/{public_id}', status_code=status.HTTP_202_ACCEPTED)
def update_image(request: schemas.Gallery, db: Session = Depends(get_db)):
    response = gallery.update(request, db)
    return {'message': response}


@router.put('/approve', status_code=status.HTTP_200_OK)
def approve_image(request: schemas.Gallery, db: Session = Depends(get_db)):
    response = gallery.approve_image(request, db)
    return response


@router.put('/approve/all/{modified_by}', status_code=status.HTTP_200_OK)
def approve_all_pending_images(modified_by: str, db: Session = Depends(get_db)):
    response = gallery.approve_all_images(modified_by, db)
    return response


@router.put('/sync', status_code=status.HTTP_200_OK)
def sync_with_offline_gallery(db: Session = Depends(get_db)):
    images = gallery.get_active_images(db)
    output = []
    for image in images:
        todo_data = {
            'id': image.id,
            'src': image.src,
            'status': image.status,
            'section': image.section,
        }
        output.append(todo_data)
    with open('gallery.json', 'w') as f:
        json.dump(output, f)

    remote_path = str(SERVER_PATH + '/data/')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('bonitohairspot.com', username='vr8hg0t7c45b', password='Bonitoadmin123')
    sftp = ssh.open_sftp()

    sftp.put('gallery.json', remote_path + 'gallery.json')
    os.remove('gallery.json')
    sftp.close()
    ssh.close()
    return {"status": "Synchronized successfully"}


@router.delete('/{public_id}', status_code=status.HTTP_200_OK)
def delete_image(public_id: str, db: Session = Depends(get_db)):
    response = gallery.delete(public_id, db)
    return {response}
