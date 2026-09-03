from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
SQLALCHEMY_DATABASE_URL = "postgresql://localhost:5432/postgres"
 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 

