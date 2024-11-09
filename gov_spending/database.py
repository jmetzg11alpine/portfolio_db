from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

name = os.getenv('POSTGRES_NAME')
host = os.getenv('POSTGRES_HOST')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')

DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
