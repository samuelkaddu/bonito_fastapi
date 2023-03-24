from pydantic import BaseModel
from pydantic.types import date


class Gallery(BaseModel):
    id: int = None
    public_id: str = None
    src: str
    status: str
    section: str
    created_by: str = None
    create_date: date = None
    modified_by: str = None
    modified_date: date = None

    class Config():
        orm_mode = True
