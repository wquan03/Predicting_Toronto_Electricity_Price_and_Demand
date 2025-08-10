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

ontario_demand_path = var.demand_input + 'Zonal\\'
df_demand = pd.read_csv(ontario_demand_path + 'PUB_DemandZonal_merged.csv')
df_demand = df_demand[['Date', 'Hour', 'Ontario Demand', 'Toronto']]
df_demand = df_demand.rename(columns = {'Toronto': 'Toronto Demand'})

# Combining date with hour
df_demand['Date'] = pd.to_datetime(df_demand['Date'], format='ISO8601')
df_demand['Date'] = df_demand['Date'] + pd.to_timedelta(df_demand['Hour'], unit='h')
df_demand = df_demand.drop('Hour', axis = 1)

# Daily average
df_demand_daily = df_demand.groupby(pd.Grouper(key='Date', freq='D'))[['Toronto Demand', 'Ontario Demand']].mean()
df_demand_daily.index = df_demand_daily.index.strftime('%Y-%m-%d')

# Monthly average
df_demand_monthly = df_demand.groupby(pd.Grouper(key='Date', freq='ME'))[['Toronto Demand', 'Ontario Demand']].mean()
df_demand_monthly.index = df_demand_monthly.index.strftime('%Y-%m')

# Output to excel
with pd.ExcelWriter(var.demand_output + 'toronto_demand_time_series_data.xlsx') as writer:
    df_demand.to_excel(writer, sheet_name='raw data', index = False)
    df_demand_daily.to_excel(writer, sheet_name='daily average')
    df_demand_monthly.to_excel(writer, sheet_name='monthly average')
print(df_demand)