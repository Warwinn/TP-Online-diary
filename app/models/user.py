from sqlalchemy import Table , Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from app.config.database import meta

users = Table(
    "user",meta,
    Column('user_id',Integer,primary_key=True),
    Column('user_name',String),
    Column('user_last_meet',DateTime),
    Column('user_next_meet',DateTime)
)
