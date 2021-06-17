#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Mergedata.py: Run for merge and split the Data use by the project."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

import sys
import pandas as pd
from sklearn.model_selection import train_test_split

sys.path.append("../src")

# Import data
df_dataK = pd.read_csv(r'./data/d02_intermediate/CleanKaggle.csv')
df_dataW = pd.read_csv(r'./data/d02_intermediate/CleanDataworld.csv')

# Merge dataframe
frames = [df_dataK , df_dataW]
df_datall = pd.concat(frames)

# Split Data Model Training and data BDD
ML, BDD = train_test_split(df_datall, test_size=0.1, random_state=1)

# Remove cache
del df_datall

# Export to CSV
BDD.to_csv("./data/d03_cleaned_data/dataBDD.csv",index=False)

# Remove cache
del BDD

# Export to CSV
ML.to_csv("./data/d03_cleaned_data/dataML.csv",index=False)

# Remove cache
del ML
