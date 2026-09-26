from sqlalchemy import Column,String,Integer,Enum,TEXT,ForeignKey
from db import get_db,Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    confirm_password=Column(String,nullable=False)
    role=Column(Enum("admin","user","guest",name="roles"),nullable=False,server_default="guest")
    number=Column(Integer,nullable=False,server_default="0")

class Notes(Base):
    __tablename__="notes"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    title=Column(String,nullable=False,unique=True)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("Now()"))
    updated_at=Column(TIMESTAMP(timezone=True),server_default=text("Now()"),onupdate=text("Now()"))
    content=Column(TEXT,nullable=False)

