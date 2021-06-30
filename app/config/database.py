#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""database.py.py: Use for connnect SQL Database and API."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

from sqlalchemy import create_engine,MetaData
from src.log import user , host , password

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:3306/Online_Diary"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
meta = MetaData()
conn = engine.connect()
