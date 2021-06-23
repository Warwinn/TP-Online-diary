import datetime
from sqlalchemy.sql import func
from operator import and_
from fastapi import APIRouter
from app.config.database import conn
from app.models.index import users,messages
from app.schemas.index import User,Message
from app.fonction.fonctionAPI import ml_emotion
user = APIRouter()

@user.get("/list_user/")
async def list_user():
    """return all user"""
    return conn.execute(users.select()).fetchall()

@user.post("/create_user/")
async def create_user(user:User):
    """use for create user"""
    conn.execute(users.insert().values(
        user_name = user.user_name,
        user_last_meet = user.user_last_meet,
        user_next_meet = user.user_next_meet)) 
    return conn.execute(users.select()).fetchall()

@user.get("/read_user/{user_id}")
async def read_user(user_id: int):
    """return data of input user"""
    return conn.execute(users.select().where(users.c.user_id==user_id)).fetchall()

@user.put("/update_user/{user_id}")
async def update_user(user_id:int,user:User):
    """use for update the data of input user"""
    conn.execute(users.update().where(users.c.user_id==user_id).values(
        user_name = user.user_name,
        user_last_meet = user.user_last_meet,
        user_next_meet = user.user_next_meet
    ))
    return conn.execute(users.select().where(users.c.user_id==user_id)).fetchall()

@user.get("/delete_user/{user_id}")
async def delete_user(user_id:int):
    """use for delete the input user"""
    conn.execute(users.delete().where(users.c.user_id == user_id))
    
    return 'successfull deleted'

@user.post("/create_message/{user_id}")
async def create_message(user_id:int,dm_text:str):
    """use for create message of user"""
    conn.execute(messages.insert().values(
    user_id = user_id  ,
    dm_text = dm_text ))
    ml_emotion(dm_text)
    return 'Message créé'

@user.put("/edit_message/{user_id}")
async def edit_message(user_id:int,dm_text:str):
    """use for edit message of user"""
    conn.execute(messages.update().values(
    user_id = user_id  ,
    dm_text = dm_text ).where(and_(messages.c.dm_datetime == datetime.date.today() , messages.c.user_id == user_id) ))
    ml_emotion(dm_text)
    return 'Message Edité'

@user.get("/list_message/{user_id}")
async def list_message(user_id:int):
    """use for list message of user"""
    return conn.execute(messages.select().where(messages.c.user_id==user_id)).fetchall()

@user.get("/read_message_emotion/{user_id}")
async def read_message_emotion(user_id:int,dm_datetime):
    """use for read the emotion for a day and user"""
    return conn.execute(messages.select().where(and_(messages.c.dm_datetime == dm_datetime,messages.c.user_id==user_id) )).fetchall()

@user.get("/read_moyenne_emotion_periode/{user_id}")
async def read_message_emotion_periode(user_id:int,debut_dm_datetime:datetime.datetime,fin_dm_datetime:datetime.datetime):
    """use for read the emotion for a day and user"""
    nb_row = conn.execute(messages.select(func.count(messages.c.dm_prob_happy)).where((messages.c.dm_datetime < debut_dm_datetime )&( messages.c.dm_datetime > fin_dm_datetime )&( messages.c.user_id == user_id)))
    print('ici')
    dm_prob_anger = conn.execute(messages.select(func.sum(messages.c.dm_prob_anger)).where(messages.c.dm_datetime < debut_dm_datetime & messages.c.dm_datetime > fin_dm_datetime & messages.c.user_id == user_id)) /nb_row
    dm_prob_fear = conn.execute(messages.select(func.sum(messages.c.dm_prob_fear)).where(and_(messages.c.dm_datetime < debut_dm_datetime,messages.c.dm_datetime > fin_dm_datetime , messages.c.user_id == user_id))) /nb_row
    dm_prob_happy = conn.execute(messages.select(func.sum(messages.c.dm_prob_happy)).where(and_(messages.c.dm_datetime < debut_dm_datetime,messages.c.dm_datetime > fin_dm_datetime , messages.c.user_id == user_id))) /nb_row
    dm_prob_love = conn.execute(messages.select(func.sum(messages.c.dm_prob_love)).where(and_(messages.c.dm_datetime < debut_dm_datetime,messages.c.dm_datetime > fin_dm_datetime , messages.c.user_id == user_id))) /nb_row
    dm_prob_sadness = conn.execute(messages.select(func.sum(messages.c.dm_prob_sadness)).where(and_(messages.c.dm_datetime < debut_dm_datetime,messages.c.dm_datetime > fin_dm_datetime , messages.c.user_id == user_id))) /nb_row
    dm_prob_surprise = conn.execute(messages.select(func.sum(messages.c.dm_prob_surprise)).where(and_(messages.c.dm_datetime < debut_dm_datetime,messages.c.dm_datetime > fin_dm_datetime , messages.c.user_id == user_id))) /nb_row
    return [dm_prob_anger,dm_prob_fear,dm_prob_happy,dm_prob_love,dm_prob_sadness,dm_prob_surprise]
