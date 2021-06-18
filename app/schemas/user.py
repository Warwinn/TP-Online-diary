from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_name:str
    user_last_meet:datetime
    user_next_meet:datetime