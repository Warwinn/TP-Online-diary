#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""routes.py: define all routes use by the api request."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

import sys
import datetime
from operator import and_
from sqlalchemy.sql import func
from fastapi import APIRouter
from app.config.database import conn
from app.models.index import users,messages
from app.schemas.index import User
from app.fonction.fonction_api import ml_emotion

sys.setrecursionlimit(15000)
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

@user.get("/read_message/{user_id}")
async def read_message(user_id: int):
    """return daily message of input user"""
    return conn.execute(messages.select()
             .where(and_(messages.c.user_id==user_id,
                        messages.c.dm_datetime == datetime.date.today())))

@user.put("/edit_message/{user_id}")
async def edit_message(user_id:int,dm_text:str):
    """use for edit message of user"""
    conn.execute(messages.update().values(
    user_id = user_id  ,
    dm_text = dm_text ).where(and_(messages.c.dm_datetime == datetime.date.today() ,
                                     messages.c.user_id == user_id) ))
    ml_emotion(dm_text)
    return 'Message Edité'

@user.get("/list_message/{user_id}")
async def list_message(user_id:int):
    """use for list message of user"""
    return conn.execute(messages.select()
                .where(messages.c.user_id==user_id)).fetchall()

@user.get("/read_message_emotion/{user_id}")
async def read_message_emotion(user_id:int,dm_datetime):
    """use for read the emotion for a day and user"""
    return conn.execute(messages.select()
            .where(and_(messages.c.dm_datetime == dm_datetime,
                        messages.c.user_id==user_id) )).fetchall()

@user.get("/read_moyenne_emotion_periode/{user_id}")
async def read_message_emotion_periode(user_id:int,
                                    debut_dm_datetime:datetime.datetime,
                                    fin_dm_datetime:datetime.datetime):
    """use for read the emotion for a day and user"""
    prob = conn.execute(messages.select(func.avg(messages.c.dm_prob_anger,
                                                messages.c.dm_prob_fear,
                                                messages.c.dm_prob_happy,
                                                messages.c.dm_prob_love,
                                                messages.c.dm_prob_sadness,
                                                messages.c.dm_prob_surprise))
                                .where( messages.c.user_id == user_id))
    return prob
