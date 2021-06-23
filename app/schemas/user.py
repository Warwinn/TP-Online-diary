from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_name:str
    user_last_meet:datetime
    user_next_meet:datetime

class Message(BaseModel):
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