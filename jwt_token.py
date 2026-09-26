from jose  import jwt 
from fastapi import  Depends
from fastapi.security.http import HTTPAuthorizationCredentials,HTTPBearer
from dotenv import load_dotenv
import os 

load_dotenv()
auth = HTTPBearer()
secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")

def create_access_token(id:int,name:str):
    payload={
        "id":id,
        "name":name
    }
    token= jwt.encode(
        payload,
        secret_key,
        algorithm
    )
    return token

def get_detail(token):
    payload=jwt.decode(token.credentials,
                       secret_key,
                       [algorithm]
                       )
    return payload

    
    
