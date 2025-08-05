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

supply_prefix = 'PUB_GenOutputbyFuelHourly_'
start_year = 2015

# Merging Dataframes
df_supply_lst = []
for year in range(start_year, var.cur_year + 1):
    df_supply = pd.read_excel(var.supply_input + 'PUB_GenOutputbyFuelHourly\\' + supply_prefix + str(year) + '.xlsx', usecols = [6, 7, 10])
    df_supply_lst.append(df_supply)
    
df_supply_final = pd.concat(df_supply_lst)

# Renaming Dataframe
df_supply_final = df_supply_final.rename(columns = {
    'ns1:Day': 'Date',
    'ns1:Hour': 'Hour',
    'ns1:Output': 'MW Amount'
})

# Combine hourly data
df_supply_final = df_supply_final.groupby(['Date', 'Hour'])['MW Amount'].sum().reset_index()

# Combining date with hour
df_supply_final['Date'] = pd.to_datetime(df_supply_final['Date'])
df_supply_final['Date'] = df_supply_final['Date'] + pd.to_timedelta(df_supply_final['Hour'], unit='h')
df_supply_final = df_supply_final.drop('Hour', axis = 1)


with pd.ExcelWriter(var.supply_input + 'PUB_GenOutputbyFuelHourly\\' + supply_prefix + 'merged.xlsx') as writer:
    df_supply_final.to_excel(writer, index = False)

