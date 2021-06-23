import datetime
import mysql.connector
import keras
import numpy as np
from src.log import host,user,password

# MYSQL Database connection

my_db = mysql.connector.connect(host=host,user=user,password=password)

my_cursor = my_db.cursor(buffered=True)
my_cursor.execute("use Online_Diary")

# Fill Message Table
model = keras.models.load_model('src/model_NLP')
list_emotion=['anger','fear','happy','love','sadness','surprise']

random_dates = datetime.date.today()
def ml_emotion(text):
    prediction_prob = model.predict([text])
    prediction= list_emotion[np.argmax(prediction_prob)]
    text = text.replace("'", "")
    text = text.replace("\\","")
    insert_daily_message = f"UPDATE daily_message SET dm_emotion='{prediction}',dm_prob_anger='{np.round(prediction_prob[0][0],6)}',dm_prob_fear='{np.round(prediction_prob[0][1],6)}',dm_prob_happy='{np.round(prediction_prob[0][2],6)}',dm_prob_love='{np.round(prediction_prob[0][3],6)}',dm_prob_sadness='{np.round(prediction_prob[0][4],6)}',dm_prob_surprise='{np.round(prediction_prob[0][5],6)}',dm_datetime='{random_dates}'WHERE dm_text = '{text}' ;"
    print(insert_daily_message)
    my_cursor.execute(insert_daily_message)
    my_db.commit()