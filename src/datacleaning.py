#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Datacleaning.py: Run for retrive the Data use by the project."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

import sys
import pandas as pd

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
    """Transform all emotion into 6 primary emotion"""
    if row == "worry":
        rtn = "fear"
    elif row == "happiness":
        rtn = "happy"
    elif row == "fun":
        rtn = "happy"
    elif row == "relief":
        rtn = "happy"
    elif row == "enthusiasm":
        rtn = "happy"
    elif row == "boredom":
        rtn = "sadness"
    elif row == "hate":
        rtn = "anger"
    else :
        rtn = row
    return rtn

df_dataW["emotion"]= df_dataW["emotion"].apply(basic_emotion)

#Remove Neutral and empty
df_dataW.drop(df_dataW[df_dataW['emotion'] == 'empty'].index,inplace=True)
df_dataW.drop(df_dataW[df_dataW['emotion'] == 'neutral'].index,inplace=True)

# Export to CSV
df_dataW.to_csv("./data/d02_intermediate/CleanDataworld.csv",index=False)

# Emptying cache
del df_dataW
