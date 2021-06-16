#!/usr/bin/env python
# -*- coding: utf-8 -*-
##################################

#################################
"""CreateDDB.py: Run for retrive the Database use by the project."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

import mysql.connector
import random
import time
import pandas as pd
import keras
import numpy as np
    
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


# Connexion à la base de données
from log import host,user,password
my_db = mysql.connector.connect(host=host,user=user,password=password)

my_cursor = my_db.cursor(buffered=True)

##################################
delete_database = "DROP DATABASE Online_Diary"
my_cursor.execute(delete_database)
#################################

# Creation de la database

my_cursor.execute("CREATE DATABASE IF NOT EXISTS Online_Diary CHARACTER SET 'utf8'")
my_cursor.execute("use Online_Diary")


# Création de la table user
my_cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(20), user_last_meet DATETIME, user_next_meet DATETIME) ENGINE = INNODB;")

# Création de la table daily_message
my_cursor.execute("CREATE TABLE IF NOT EXISTS daily_message (dm_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, user_id SMALLINT UNSIGNED, dm_text TEXT, dm_emotion VARCHAR(100), dm_datetime DATETIME, FOREIGN KEY (user_id) REFERENCES user(user_id) ON UPDATE CASCADE ON DELETE CASCADE)ENGINE = INNODB;")
my_db.commit()

# Generaton de client

client=['iveline', 'badisse', 'ulisse', 'yohanna', 'chafiha', 'septi', 'anne-soazig', 'rona', 'guy-marie', 'ehouarn', 'emily', 'abdelillah', 'perrick',
'haytem', 'farouck', 'semir', 'ria', 'kaiser', 'khalifa', 'ikbal', 'marie-vanessa', 'pierre-bertrand', 'florane', 'nour-imene', 'souria', 'tany',
'ilan' , 'rojhat', 'peters', 'maelline']

rand = random.randint(5,30)
selected_client = random.sample(client,rand)

import datetime
for client in selected_client:
    last_meet = datetime.date.today() #random_date("01/01/2021 00:00 AM", "06/01/2021 00:00 AM", random.random())
    next_meet = last_meet + datetime.timedelta(days=7)
    insert_client = f"INSERT INTO user (user_id, user_name, user_last_meet, user_next_meet) VALUES (null, '{client}', '{last_meet}', '{next_meet}');"
    my_cursor.execute(insert_client)
my_db.commit()

# Import Text for Database
df_BDD = pd.read_csv(r'./data/d03_cleaned_data/dataBDD.csv')
############################
df_BDD = df_BDD.sample(100)
############################
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
for text in df_BDD['text']:
    random_dates= datetime.date.today() #random_date("01/01/2021 00:00 AM", "06/01/2021 00:00 AM", random.random())
    prediction= np.argmax(model.predict([text]))
    prediction= list_emotion[prediction]
    text = text.replace("'", "")
    insert_daily_message = f"INSERT INTO daily_message VALUES  (null, '{random.choice(list_client_ids)}', '{text}','{prediction}', '{random_dates}');"
    my_cursor.execute(insert_daily_message)
    my_db.commit()
