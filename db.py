from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os

url=os.getenv("DATABASE_URL")
engine=create_engine(url)
sl=sessionmaker(bind=engine,
                autoflush=True,
    )
Base=declarative_base()

def get_db():
    db=sl()
    try:
        yield db
    finally:
        db.close()


