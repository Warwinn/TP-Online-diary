#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""fonctionAPI.py: Store fonction for thr API."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

import datetime
import mysql.connector
import keras
import numpy as np
from src.log import host,user,password

# MYSQL Database connection

my_db = mysql.connector.connect(host=host,user=user,password=password)
my_cursor = my_db.cursor(buffered=True)
my_cursor.execute("use Online_Diary")

model = keras.models.load_model('src/model_NLP')
list_emotion=['anger','fear','happy','love','sadness','surprise']
random_dates = datetime.date.today()

def ml_emotion(text):
    """Use the model for predict the emotion and add it into the database"""
    prediction_prob = model.predict([text])
    prediction= list_emotion[np.argmax(prediction_prob)]
    text = text.replace("'", "")
    text = text.replace("\\","")
    insert_daily_message = f"UPDATE daily_message SET dm_emotion='{prediction}',dm_prob_anger='{np.round(prediction_prob[0][0],6)}',dm_prob_fear='{np.round(prediction_prob[0][1],6)}',dm_prob_happy='{np.round(prediction_prob[0][2],6)}',dm_prob_love='{np.round(prediction_prob[0][3],6)}',dm_prob_sadness='{np.round(prediction_prob[0][4],6)}',dm_prob_surprise='{np.round(prediction_prob[0][5],6)}',dm_datetime='{random_dates}'WHERE dm_text = '{text}' ;"
    print(insert_daily_message)
    my_cursor.execute(insert_daily_message)
    my_db.commit()
    