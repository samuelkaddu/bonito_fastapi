import datetime
import os
import shutil
import uuid
from typing import List

import paramiko
from fastapi import APIRouter, Depends, status, Request, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from api import database, models

router = APIRouter(
    prefix="/upload",
    tags=['Uploads']
)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# SERVER_PATH = "public_html/dev.test.bonitohairspot.com"
SERVER_PATH = "public_html"

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
async def upload_file(request: Request, images: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        sub_path = request.headers.get('sub_path') + "/"
        target = request.headers.get('target_section')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('bonitohairspot.com', username='vr8hg0t7c45b', password='Bonitoadmin123')
        remote_path = str(SERVER_PATH + sub_path)

        for image in images:
            new_image_gallery = models.Gallery(
                public_id=str(uuid.uuid4()),
                src=sub_path + image.filename,
                status='Submitted',
                section=target,
                created_by='SYSTEM',
                create_date=datetime.datetime.now().date()
            )
            db.add(new_image_gallery)
            sftp = ssh.open_sftp()
            tmp_dir = 'tmp'
            with open(f"tmp/{image.filename}", "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            sftp.put(os.path.join(tmp_dir, secure_filename(image.filename)), remote_path + image.filename)
            os.remove(os.path.join(tmp_dir, image.filename))

        db.commit()
        db.refresh(new_image_gallery)
        sftp.close()
        ssh.close()
        response = JSONResponse({"code": "0", "message": "Success"})
        return response
    except Exception as e:
        sftp.close()
        ssh.close()
        response = JSONResponse({"code": "99", "message": "Operation failed"})
        return response


@router.post('/remove', status_code=status.HTTP_200_OK)
async def remove_file(request: Request, images: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        data = request.get_json()
        # Create an SSH connection to the Linux server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('bonitohairspot.com', username='vr8hg0t7c45b', password='Bonitoadmin123')

        # Remove the file from the server
        ssh.exec_command('rm {}'.format(SERVER_PATH + data['path'] + data['name']))

        # Close the SSH connection
        ssh.close()

        response = JSONResponse({"code": "0", "message": 'File {} removed successfully'})

        return response
    except paramiko.ssh_exception.AuthenticationException:
        response = JSONResponse({"code": "99", "message": 'Could not authenticate with server'})
        response.status_code = 500
        return response

    except paramiko.ssh_exception.SSHException:
        response = JSONResponse({"code": "99", "message": 'Could not establish SSH connection to server'})
        return response
    except Exception as e:
        response = JSONResponse({"code": "99", "message": 'Error occurred: {}'.format(e)})
        return response
        return response
