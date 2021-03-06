#!/usr/bin/env python
# -*- coding: utf-8 -*
"""CreateDDB.py: Run for retrive the Database use by the project."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

import sys
import datetime

import random
import pandas as pd
import keras
import numpy as np
import mysql.connector
from log import host,user,password
from faker import Faker

sys.path.append("./TP-Online-diary")
sys.path.append("./data")

fake=Faker()

# MYSQL Database connection

my_db = mysql.connector.connect(host=host,user=user,password=password)

my_cursor = my_db.cursor(buffered=True)

# Create Database

my_cursor.execute("CREATE DATABASE IF NOT EXISTS Online_Diary CHARACTER SET 'utf8'")
my_cursor.execute("use Online_Diary")


# Create Tables
my_cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(20), user_last_meet DATETIME, user_next_meet DATETIME) ENGINE = INNODB;")
my_cursor.execute("CREATE TABLE IF NOT EXISTS daily_message (dm_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, user_id SMALLINT UNSIGNED, dm_text TEXT, dm_emotion VARCHAR(100), dm_prob_anger DECIMAL(7,6), dm_prob_fear DECIMAL(7,6), dm_prob_happy DECIMAL(7,6), dm_prob_love DECIMAL(7,6),dm_prob_sadness DECIMAL(7,6),dm_prob_surprise DECIMAL(7,6), dm_datetime DATETIME, FOREIGN KEY (user_id) REFERENCES user(user_id) ON UPDATE CASCADE ON DELETE CASCADE)ENGINE = INNODB;")
my_db.commit()

# Randomise quantity and client name

client=['iveline', 'badisse', 'ulisse', 'yohanna', 'chafiha', 'septi', 'anne-soazig', 'rona',
'guy-marie', 'ehouarn', 'emily', 'abdelillah', 'perrick','haytem', 'farouck', 'semir', 'ria',
'kaiser', 'khalifa', 'ikbal', 'marie-vanessa', 'pierre-bertrand', 'florane', 'nour-imene',
'souria', 'tany','ilan' , 'rojhat', 'peters', 'maelline']

rand = random.randint(5,30)
selected_client = random.sample(client,rand)

# Fill User Table
for client in selected_client:
    last_meet = fake.date_between(start_date='-1y', end_date='-1m')
    next_meet = last_meet + datetime.timedelta(days=7)
    insert_client = f"INSERT INTO user (user_id, user_name, user_last_meet, user_next_meet) VALUES (null, '{client}', '{last_meet}', '{next_meet}');"
    my_cursor.execute(insert_client)
my_db.commit()

# Import Text and model for Database
df_BDD = pd.read_csv(r'./data/d03_cleaned_data/dataBDD.csv')
my_cursor.execute("SELECT user_id FROM user")

list_client_id=[]
list_client_ids=[]
for user_id in my_cursor:
    list_client_id.append(str(user_id))
for user_id in list_client_id:
    user_id =''.join(e for e in user_id if e.isalnum())
    list_client_ids.append(str(user_id))
model = keras.models.load_model('src/model_NLP')
list_emotion=['anger','fear','happy','love','sadness','surprise']

# Fill Message Table
for text in df_BDD['text']:
    random_dates = fake.date_between(start_date='-1y', end_date='-1m')
    prediction_prob = model.predict([text])
    prediction= list_emotion[np.argmax(prediction_prob)]
    text = text.replace("'", "")
    text = text.replace("\\","")
    insert_daily_message = f"INSERT INTO daily_message VALUES  (null, '{random.choice(list_client_ids)}', '{text}','{prediction}','{np.round(prediction_prob[0][0],6)}','{np.round(prediction_prob[0][1],6)}', '{np.round(prediction_prob[0][2],6)}','{np.round(prediction_prob[0][3],6)}','{np.round(prediction_prob[0][4],6)}','{np.round(prediction_prob[0][5],6)}','{random_dates}');"
    my_cursor.execute(insert_daily_message)
    my_db.commit()
