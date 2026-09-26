from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
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


