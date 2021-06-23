from sqlalchemy import Table , Column
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String
from app.config.database import meta

users = Table(
    "user",meta,
    Column('user_id',Integer,primary_key=True),
    Column('user_name',String),
    Column('user_last_meet',DateTime),
    Column('user_next_meet',DateTime)
)
messages = Table(
        "daily_message",meta,
    Column('dm_id',Integer,primary_key=True),
    Column('user_id',String),
    Column('dm_text',String),
    Column('dm_emotion',String),
    Column('dm_prob_anger',Float),
    Column('dm_prob_fear',Float),
    Column('dm_prob_happy',Float),
    Column('dm_prob_love',Float),
    Column('dm_prob_sadness',Float),
    Column('dm_prob_surprise',Float),
    Column('dm_datetime',DateTime))