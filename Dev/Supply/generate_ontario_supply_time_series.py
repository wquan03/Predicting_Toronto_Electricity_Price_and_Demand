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


print(project_root)

from utilities import variables as var

df_canada = pd.read_excel(var.supply_canada_stats + 'cananda_stats_merged.xlsx')
df_goc = pd.read_excel(var.supply_input + 'GOC\\GOC-merged.xlsx')
df_pub = pd.read_excel(var.supply_input + 'PUB_GenOutputbyFuelHourly\\PUB_GenOutputbyFuelHourly_merged.xlsx')


df_supply = pd.concat([df_canada, df_goc, df_pub])


# Daily average
df_supply_daily = df_supply.groupby(pd.Grouper(key='Date', freq='D'))['MW Amount'].sum().reset_index()
df_supply_daily['Date'] = df_supply_daily['Date'].dt.strftime('%Y-%m-%d')
df_supply_daily['MW Amount'] = df_supply_daily.apply(lambda row: row['MW Amount'] / 24, axis=1)

# Monthly average
df_supply_monthly = df_supply.groupby(pd.Grouper(key='Date', freq='ME'))['MW Amount'].sum().reset_index()
df_supply_monthly['Date'] = df_supply_monthly['Date'].dt.strftime('%Y-%m')
df_supply_monthly['MW Amount'] = df_supply_monthly.apply(lambda row: row['MW Amount'] / pd.Timestamp(row['Date']).days_in_month / 24, axis=1)


# Output to excel
with pd.ExcelWriter(var.supply_output + 'ontario_supply_time_series_data.xlsx') as writer:
    df_supply.to_excel(writer, sheet_name='cleaned raw data', index = False)
    
    # By month and day
    df_supply_daily.to_excel(writer, sheet_name='daily average', index = False)
    df_supply_monthly.to_excel(writer, sheet_name='monthly average', index = False)
    

