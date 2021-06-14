#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""DatacleaningMVP.py: Run for retrive the Data use by the project."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

# Import Pandas
import pandas as pd

# Set Relative Path
import sys
sys.path.append("./TP-Online-diary")
sys.path.append("./data")

# Import data
df_dataK = pd.read_csv(r'./data/d01_raw/Emotion_Kaggle.csv')

# Rename column
df_dataK.rename(columns={"Text":"text","Emotion":"emotion"},inplace=True)

# Delete duplicates
df_dataK.drop_duplicates(inplace=True)

# Export to CSV
df_dataK.to_csv("./data/d02_intermediate/CleanKaggle.csv",index=False)

# Emptying cache
del df_dataK

#Import data
df_dataW = pd.read_csv(r'./data/d01_raw/Emotion_Dataworld.csv')

# Select Data
df_dataW = df_dataW[["sentiment","content"]] 

# Rename column
df_dataW.rename(columns={"content":"text","sentiment":"emotion"},inplace=True)

# Delete duplicates
df_dataW.drop_duplicates(inplace=True)

# Transform to Basic emotion
def basic_emotion(row):
    
    if row == "worry":
        return "fear"
    elif row == "happiness":
        return "happy"
    elif row == "fun":
        return "happy"
    elif row == "relief":
        return "happy"
    elif row == "enthusiasm":
        return "happy"
    elif row == "boredom":
        return "sadness"
    elif row == "hate":
        return "anger"   
    else :
        return row

df_dataW["emotion"]= df_dataW["emotion"].apply(basic_emotion)

#Remove Neutral and empty
df_dataW.drop(df_dataW[df_dataW['emotion'] == 'empty'].index,inplace=True)
df_dataW.drop(df_dataW[df_dataW['emotion'] == 'neutral'].index,inplace=True)

# Export to CSV
df_dataW.to_csv("./data/d02_intermediate/CleanDataworld.csv",index=False)

# Emptying cache
del df_dataW