from fastapi import APIRouter
from app.config.database import conn
from app.models.index import users
from app.schemas.index import User

user = APIRouter()

@user.get("/")
async def list_user():
    """return all user"""
    return conn.execute(users.select()).fetchall()

@user.post("/")
async def create_user(user:User):
    """use for create user"""
    conn.execute(users.insert().values(
        user_name = user.user_name,
        user_last_meet = user.user_last_meet,
        user_next_meet = user.user_next_meet)) 
    return conn.execute(users.select()).fetchall()

@user.get("/read/{user_id}")
async def read_user(user_id: int):
    """return data of input user"""
    return conn.execute(users.select().where(users.c.user_id==user_id)).fetchall()

@user.put("/update/{user_id}")
async def update_user(user_id:int,user:User):
    """use for update the data of input user"""
    conn.execute(users.update().where(users.c.user_id==user_id).values(
        user_name = user.user_name,
        user_last_meet = user.user_last_meet,
        user_next_meet = user.user_next_meet
    ))
    return conn.execute(users.select().where(users.c.user_id==user_id)).fetchall()

@user.get("/delete/{user_id}")
async def delete_user(user_id:int):
    """use for delete the input user"""
    conn.execute(users.delete().where(users.c.user_id==user_id))
    
    return 'successfull deleted'