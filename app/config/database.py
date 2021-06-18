from sqlalchemy import create_engine,MetaData
from src.log import user , host , password 

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:3306/Online_Diary"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
meta = MetaData()
conn = engine.connect()