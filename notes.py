from fastapi import FastAPI,Depends
from model import User,Notes
from db  import get_db,Base,engine
from pydantic_model import signup,notes
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from jwt_token import get_detail,create_access_token
from sqlalchemy import TEXT,text
from datetime import datetime


auth=HTTPBearer()
app =FastAPI()

@app.post("/create_user")
def create_user(u:signup,db:Session=Depends(get_db)):
    db_user=User(**u.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "msg":"success",
        "id":db_user.id,
        "number":db_user.number
    }

@app.get("/user_login")
def user_login(id:int,email:str,name:str,db:Session=Depends(get_db)):
    db_user=db.query(User).filter_by(email=email).first()
    if not db_user:
        return {
            "msg":"login required"
        }
    token=create_access_token(id,name)
    return {
        "token":token
        }

@app.post("/notes_create")
def notes_create(n:notes,db:Session=Depends(get_db),token:HTTPAuthorizationCredentials=Depends(auth)):
    payload = get_detail(token)
    if not token:
        return {"msg":"token is missing"}
    if not payload:
        return {
            "msg":"missing payload"
        }
    user_id=payload.get("id")
    db_id=db.query(User).filter_by(id=user_id).first()
    if not db_id:
        return{
            "msg":"user_not_found"
        }
    db_notes=Notes(**n.model_dump())
    db.add(db_notes)
    db.commit()
    db.refresh(db_notes)
    return {
        "msg":"successfull"
    }

@app.get("/get_single_notes")
def get_single_notes(id:int,title:str,db:Session=Depends(get_db)):
    db_notes=db.query(Notes).filter_by(user_id=id,title=title).first()
    if not db_notes:
        return{"msg":"notes_not_found/not_created"}
    return {
        "content":db_notes.content
    }

@app.get("/get_notes")
def get_notes(id:int,limit:int,page:int,db:Session=Depends(get_db)):
    db_notes=db.execute(text("""
SELECT content FROM Notes
WHERE user_id=:id

    """),{"id":id})

    rows = db_notes.fetchall()
    print(rows)
    return [dict(row._mapping) for row in rows]

@app.get("/get_users")
def get_users(page:int,limit:int,db:Session=Depends(get_db)):
    db_users=db.query(User).limit(limit).offset((page-1)*limit).all()
    return {
        "msg":f"list of users in page{page} with the limit{limit}",
        "users":db_users
    }

@app.patch("/update_notes")
def update_notes(id:int,notes:str,db:Session=Depends(get_db)):
    db_user=db.query(Notes).filter_by(user_id=id).first()
    if not db_user:
        return {"msg":"user_not_found"}
    db_user.content = notes
    db_user.updated_at=datetime.now()
    db.commit()
    db.refresh(db_user)
    return {"msg":"successfull",
            "user":db_user}
    
@app.delete("/delete_user")    
def delete_user(id:int,db:Session=Depends(get_db)):
    db_user=db.query(User).filter_by(id=id).first()
    if not db_user:
        return{"msg":"user_not_found"}
    db.delete(db_user)
    db.commit()
    return{"msg":"user_deleted_successfully"}

@app.delete("/delete_all")
def delete_all(db:Session=Depends(get_db)):
    db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    db.commit()
    d_base=db.query(User).all()
    return d_base

@app.patch("/update_user")
def update_user(id:int,db:Session=Depends(get_db)):
    db_users=db.query(User).filter_by(id=id).update({User.number:User.number+1})
    db.commit()
    db.refresh(db_users)
    return "success"

Base.metadata.create_all(bind=engine)




