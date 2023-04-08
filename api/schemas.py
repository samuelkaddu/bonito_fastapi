from pydantic import BaseModel
from pydantic.types import date


class Gallery(BaseModel):
    id: int = None
    public_id: str = None
    src: str = None
    status: str = None
    section: str = None
    created_by: str = None
    create_date: date = None
    modified_by: str = None
    modified_date: date = None

    class Config():
        orm_mode = True


class User(BaseModel):
    id: int = None
    public_id: str = None
    username: str = None
    password: str = None
    isAdmin: bool = False
    status: str = None
    email: str = None
    firstname: str = None
    lastname: str = None
    isApprover: bool = False
    isReceiveMail: bool = False
    role: int = None
    resetPassword: bool = False
    created_by: str = None
    create_date: str = None
    modified_by: str = None
    modified_date: date = None

    class Config():
        orm_mode = True


class Service(BaseModel):
    id: int = None
    public_id: str = None
    name: str = None
    image_url: str = None
    status: str = None
    section: str = None
    create_date: date = None
    created_by: str = None
    modified_by: str = None
    modified_date: date = None

    class Config():
        orm_mode = True
