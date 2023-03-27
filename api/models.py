import datetime

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(80))
    isAdmin = Column(Boolean())
    status = Column(String(8), nullable=False)
    email = Column(String(50))
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    isApprover = Column(Boolean(), nullable=False)
    isReceiveMail = Column(Boolean(), nullable=False)
    role = Column(Integer, nullable=False)
    resetPassword = Column(Boolean(), nullable=False)
    created_by = Column(String(10), nullable=False)
    create_date = Column(Date, nullable=False, default=datetime.datetime.now().date())
    modified_by = Column(String(10))
    modified_date = Column(Date)


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    name = Column(String(50), unique=True)
    image_url = Column(String(50), nullable=False)
    status = Column(String(10), nullable=False)
    section = Column(String(20), nullable=False)
    created_by = Column(String(10), nullable=False)
    create_date = Column(Date, nullable=False, default=datetime.datetime.now().date())
    modified_by = Column(String(10))
    modified_date = Column(Date)


class ServiceListing(Base):
    __tablename__ = 'service_listing'
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    name = Column(String(100), nullable=False)
    service_id = Column(String(50), ForeignKey('services.public_id'))
    status = Column(String(8), nullable=False)
    created_by = Column(String(10), nullable=False)
    create_date = Column(Date, nullable=False, default=datetime.datetime.now().date())
    modified_by = Column(String(10))
    modified_date = Column(Date)
    service = relationship("Service", backref="service_listing")
