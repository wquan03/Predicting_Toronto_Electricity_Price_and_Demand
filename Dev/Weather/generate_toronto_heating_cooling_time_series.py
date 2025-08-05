import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import re
import openpyxl
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utilities import variables as var


df_temperature = pd.read_csv(var.weather_input + 'CYYZ Heating Cooling Combined.csv')


df_temperature['Date'] = pd.to_datetime(df_temperature['Date'])
# Monthly average
df_temperature_monthly_avg = df_temperature.groupby(pd.Grouper(key='Date', freq='ME'))[['HDD 15.5', 'CDD 15.5']].mean().reset_index()

# Yearly average
df_temperature_yearly_avg = df_temperature.groupby(pd.Grouper(key='Date', freq='YE'))[['HDD 15.5', 'CDD 15.5']].mean().reset_index()


# Output to excel
with pd.ExcelWriter(var.weather_output + 'heating_cooling_demand_time_series_data.xlsx') as writer:
    df_temperature.to_excel(writer, sheet_name='cleaned raw data', index=False)

    df_temperature_monthly_avg.to_excel(writer, sheet_name='Monthly Average', index=False)
    df_temperature_yearly_avg.to_excel(writer, sheet_name='Yearly Average', index=False)
