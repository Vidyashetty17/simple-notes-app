from pydantic import BaseModel
from datetime import datetime

class signup(BaseModel):
    name:str
    email:str
    password:str
    confirm_password:str
    role:str

class notes(BaseModel):
    user_id:int
    title:str
    created_at:datetime
    updated_at: datetime
    content:str


