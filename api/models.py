import datetime

from sqlalchemy import Column, Integer, String, Date

from .database import Base


class Gallery(Base):
    __tablename__ = 'gallery'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    src = Column(String(50), nullable=False)
    status = Column(String(9), nullable=False)
    section = Column(String(20), nullable=False)
    created_by = Column(String(10), nullable=False)
    create_date = Column(Date, nullable=False, default=datetime.datetime.now().date())
    modified_by = Column(String(10))
    modified_date = Column(Date)
