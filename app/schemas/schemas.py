#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""schemas.py: store the schemas architecture of the SQL database."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    """Class of User Table"""
    user_name:str
    user_last_meet:datetime
    user_next_meet:datetime

class Message(BaseModel):
    """Class of Message Table"""
    user_id:int
    dm_text:str
    dm_emotion:str
    dm_prob_anger:float
    dm_prob_fear:float
    dm_prob_happy:float
    dm_prob_love:float
    dm_prob_sadness:float
    dm_prob_surprise:float
    dm_prob_anger:float
    dm_datetime:datetime
