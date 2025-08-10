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

supply_prefix = 'GOC-'
start_year = 2010
end_year = 2014

# Merging Dataframes
df_supply_lst = []
for year in range(start_year, end_year + 1):
    df_supply = pd.read_excel(var.supply_input + 'GOC\\' + supply_prefix + str(year) + '.xlsx', sheet_name = 'Output')
    df_supply = df_supply.rename(columns = {
    'DATE': 'Date',
    'HOUR': 'Hour'
    })
    df_supply_lst.append(df_supply)

df_supply_final = pd.concat(df_supply_lst)

# Combine hourly data
generator_list = df_supply_final.columns.to_list()
generator_list.remove('Date')
generator_list.remove('Hour')
df_supply_final['MW Amount'] = df_supply_final[generator_list].sum(axis=1, numeric_only=True)

# Rename column names
df_supply_final = df_supply_final[['Date', 'Hour', 'MW Amount']]

# Combining date with hour
df_supply_final['Date'] = pd.to_datetime(df_supply_final['Date'], format='ISO8601')
df_supply_final['Date'] = df_supply_final['Date'] + pd.to_timedelta(df_supply_final['Hour'], unit='h')
df_supply_final = df_supply_final.drop('Hour', axis = 1)



with pd.ExcelWriter(var.supply_input + 'GOC\\' + supply_prefix + 'merged.xlsx') as writer:
    df_supply_final.to_excel(writer, index = False)



