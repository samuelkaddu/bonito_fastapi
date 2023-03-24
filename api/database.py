from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://bonitouser:Bonitoadmin123@72.167.126.202:3306/bonito_site"

# Create a SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Define a database model
Base = declarative_base()


# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
