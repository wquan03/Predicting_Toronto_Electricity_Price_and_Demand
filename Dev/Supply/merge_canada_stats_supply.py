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

# archive data, up to 2007-12
df_supply1 = pd.read_csv(var.supply_canada_stats + '2002 05 - 2007 12.csv')
df_supply1 = df_supply1[['REF_DATE', 'Electric power, components', 'VALUE']]
df_supply1 = df_supply1.rename(columns={'REF_DATE': 'Date', 'Electric power, components': 'Type of electricity generation', 'VALUE': 'MW Amount'})
df_supply1 = df_supply1.loc[df_supply1['Type of electricity generation'] == 'Overall total generation']


# present data, up to 2025-04
df_supply2 = pd.read_csv(var.supply_canada_stats + '2008 01 - 2025 04.csv')
df_supply2 = df_supply2[['REF_DATE', 'Type of electricity generation', 'VALUE']]
df_supply2 = df_supply2.rename(columns={'REF_DATE': 'Date', 'VALUE': 'MW Amount'})
df_supply2 = df_supply2.loc[df_supply2['Type of electricity generation'] == 'Total all types of electricity generation']


# combine archive and present data
df_supply = pd.concat([df_supply1, df_supply2])
df_supply = df_supply.drop('Type of electricity generation', axis = 1)
df_supply = df_supply.rename(columns={'REF_DATE': 'Date'})

# convert unit, MWh -> MW
df_supply['MW Amount'] = df_supply.apply(lambda row: row['MW Amount'] / pd.Timestamp(row['Date']).days_in_month / 24, axis=1)

# For future, can add in fuel type based MW
df_supply = df_supply.loc[pd.to_datetime(df_supply['Date']).dt.year < 2010]

# Expand to daily formate
df_supply['Date'] = pd.to_datetime(df_supply['Date'], format='%Y-%m')
expanded_rows = []
for _, row in df_supply.iterrows():
    start = row['Date']
    end = (start + pd.offsets.MonthEnd(1)).replace(hour=23)
    
    # Generate hourly datetime range for the month
    hourly_range = pd.date_range(start=start, end=end, freq='h')
    
    # Create hourly rows
    for hour in hourly_range:
        expanded_rows.append({'Date': hour, 'MW Amount': row['MW Amount']})

# Create the exploded DataFrame
daily_df = pd.DataFrame(expanded_rows)

# Output to excel
with pd.ExcelWriter(var.supply_canada_stats + 'cananda_stats_merged.xlsx') as writer: 
    daily_df.to_excel(writer, sheet_name='monthly average', index = False)

    

