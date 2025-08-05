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


df_supply = pd.read_csv(var.supply_root + 'PUB_GenOutputCapability_Merged.csv')

# Transpose all the hour columns
df_supply_cleaned = df_supply.melt(
    id_vars=['Delivery Date', 'Generator', 'Fuel Type', 'Measurement'],
    var_name='Hour',
    value_name='MW Amount'
)
df_supply_cleaned['Hour'] = df_supply_cleaned['Hour'].str.extract('Hour (\d+)').astype(int)

# Combining date with hour
df_supply_cleaned['Delivery Date'] = pd.to_datetime(df_supply_cleaned['Delivery Date'])
df_supply_cleaned['Delivery Date'] = df_supply_cleaned['Delivery Date'] + pd.to_timedelta(df_supply_cleaned['Hour'], unit='h')
df_supply_cleaned = df_supply_cleaned.drop('Hour', axis = 1)

# drop unwanted column
df_supply_cleaned = df_supply_cleaned.drop('Generator', axis = 1)

# data quality check
df_supply_cleaned['MW Amount'] = df_supply_cleaned['MW Amount'].fillna(0)
df_supply_cleaned['MW Amount'] = pd.to_numeric(df_supply_cleaned['MW Amount'], errors='coerce').fillna(0).astype(int)

# Combine duplicate keys with group by
df_supply_cleaned = df_supply_cleaned.groupby(['Delivery Date', 'Fuel Type', 'Measurement'])['MW Amount'].sum().reset_index()


# Separating the different measurement
df_supply_output = df_supply_cleaned.loc[df_supply_cleaned['Measurement'] == 'Output']
df_supply_capacity = df_supply_cleaned.loc[df_supply_cleaned['Measurement'] == 'Capability']
df_supply_available_capacity = df_supply_cleaned.loc[df_supply_cleaned['Measurement'] == 'Available Capacity']
df_supply_total_capacity = pd.concat([df_supply_capacity, df_supply_available_capacity])

# Drop the column measurement
df_supply_output = df_supply_output.drop('Measurement', axis = 1)
df_supply_total_capacity = df_supply_total_capacity.drop('Measurement', axis = 1)





# Daily average
df_supply_output_daily_sum = df_supply_output.groupby('Delivery Date')['MW Amount'].sum().reset_index()
df_supply_total_capacity_daily_sum = df_supply_total_capacity.groupby('Delivery Date')['MW Amount'].sum().reset_index()

df_supply_output_daily = df_supply_output_daily_sum.groupby(pd.Grouper(key='Delivery Date', freq='D'))['MW Amount'].mean().reset_index()
df_supply_output_daily['Delivery Date'] = df_supply_output_daily['Delivery Date'].dt.strftime('%Y-%m-%d')

df_supply_total_capacity_daily = df_supply_total_capacity_daily_sum.groupby(pd.Grouper(key='Delivery Date', freq='D'))['MW Amount'].mean().reset_index()
df_supply_total_capacity_daily['Delivery Date'] = df_supply_total_capacity_daily['Delivery Date'].dt.strftime('%Y-%m-%d')

# Monthly average
df_supply_output_monthly = df_supply_output_daily_sum.groupby(pd.Grouper(key='Delivery Date', freq='M'))['MW Amount'].mean().reset_index()
df_supply_output_monthly['Delivery Date'] = df_supply_output_monthly['Delivery Date'].dt.strftime('%Y-%m')

df_supply_total_capacity_monthly = df_supply_total_capacity_daily_sum.groupby(pd.Grouper(key='Delivery Date', freq='M'))['MW Amount'].mean().reset_index()
df_supply_total_capacity_monthly['Delivery Date'] = df_supply_total_capacity_monthly['Delivery Date'].dt.strftime('%Y-%m')

# Daily average by fuel type
df_supply_output_daily_fuel = df_supply_output.groupby([pd.Grouper(key='Delivery Date', freq='D'), 'Fuel Type'])['MW Amount'].mean().reset_index()
df_supply_output_daily_fuel['Delivery Date'] = df_supply_output_daily_fuel['Delivery Date'].dt.strftime('%Y-%m-%d')

df_supply_total_capacity_daily_fuel = df_supply_total_capacity.groupby([pd.Grouper(key='Delivery Date', freq='D'), 'Fuel Type'])['MW Amount'].mean().reset_index()
df_supply_total_capacity_daily_fuel['Delivery Date'] = df_supply_total_capacity_daily_fuel['Delivery Date'].dt.strftime('%Y-%m-%d')

# Monthly average by fuel type
df_supply_output_monthly_fuel = df_supply_output.groupby([pd.Grouper(key='Delivery Date', freq='M'), 'Fuel Type'])['MW Amount'].mean().reset_index()
df_supply_output_monthly_fuel['Delivery Date'] = df_supply_output_monthly_fuel['Delivery Date'].dt.strftime('%Y-%m')

df_supply_total_capacity_monthly_fuel = df_supply_total_capacity.groupby([pd.Grouper(key='Delivery Date', freq='M'), 'Fuel Type'])['MW Amount'].mean().reset_index()
df_supply_total_capacity_monthly_fuel['Delivery Date'] = df_supply_total_capacity_monthly_fuel['Delivery Date'].dt.strftime('%Y-%m')

# # Output to excel
# with pd.ExcelWriter(var.supply_root + 'cleaned_supply.xlsx') as writer: 
#     df_supply_cleaned.to_excel(writer, sheet_name='cleaned raw data', index = False)
    
#     # By month and day
#     df_supply_output_daily.to_excel(writer, sheet_name='D avg output', index = False)
#     df_supply_total_capacity_daily.to_excel(writer, sheet_name='D avg capacity', index = False)
#     df_supply_output_monthly.to_excel(writer, sheet_name='M avg output', index = False)
#     df_supply_total_capacity_monthly.to_excel(writer, sheet_name='M avg capacity', index = False)
    
#     # By month and day and fuel type
#     df_supply_output_daily_fuel.to_excel(writer, sheet_name='D avg output by fuel type', index = False)
#     df_supply_total_capacity_daily_fuel.to_excel(writer, sheet_name='D avg capacity by fuel type', index = False)
#     df_supply_output_monthly_fuel.to_excel(writer, sheet_name='M avg output by fuel type', index = False)
#     df_supply_total_capacity_monthly_fuel.to_excel(writer, sheet_name='M avg capacity by fuel type', index = False)
    

