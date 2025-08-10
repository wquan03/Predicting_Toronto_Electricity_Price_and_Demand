import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import reduce
import warnings
import re
import openpyxl
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys


project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utilities import variables as var

df_all_field = pd.read_excel(var.anaylsis_output + 'all_field_data_daily.xlsx', sheet_name = 'All Data Fields')  # Change this to the actual filename
field_lst = var.model_field_lst

df_all_field = df_all_field[['Date'] + field_lst]
df_all_field = df_all_field.drop(0)


# copied from gpt
threshold = df_all_field['Price'].quantile(0.90)
df_all_field['Spike'] = (df_all_field['Price'] > threshold).astype(int)

features = [
    var.toronto_temp,
    var.toronto_humidity,
    var.toronto_dew_point,
    var.toronto_wing_speed,
    var.toronto_sea_level_pressure, 
    var.toronto_precipitation,
    var.hdd_15,
    var.cdd_15,
    var.hdd_18,
    var.cdd_18
]

X = df_all_field[features]
y = df_all_field['Spike']

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X_train, y_train)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

spike_probs = model.predict_proba(X_test)[:, 1]  # probability of class "1"


future_input = pd.DataFrame([{
    var.toronto_temp: 25,
    var.toronto_humidity: 52.7,
    var.toronto_dew_point: 18.4,
    var.toronto_wing_speed: 6.58,
    var.toronto_sea_level_pressure: 0, 
    var.toronto_precipitation: 101.52,
    var.hdd_15: 0,
    var.cdd_15: 10,
    var.hdd_18: 0,
    var.cdd_18: 7
}])


future_prob = model.predict_proba(future_input)[:, 1]
print(f"Chance of price/demand spike: {future_prob[0]*100:.2f}%")