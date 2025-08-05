import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import re
import openpyxl
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys

# base_root = 'C:\\Users\\CGOD\\Desktop\\University\\ROP\\IESO MRP Data\\'
# sys.path.append(base_root)

# from utilities import variables as var

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utilities import variables as var


df_price = pd.read_excel(var.market_price_input + 'Nodal Price\\PUB_PriceNodal_merged.xlsx')


# Pre-process the data
df_price = df_price.rename(columns = {'Darlington': 'Price'})
df_price['Price'] = df_price['Price'].fillna(0)


# df_price['Price'] = df_price['Price'].astype(str).str.replace(',', '').astype(float)


# Daily average
df_price_daily = df_price.groupby(pd.Grouper(key='Date', freq='D'))['Price'].mean()
df_price_daily.index = df_price_daily.index.strftime('%Y-%m-%d')

# Monthly average
df_price_monthly = df_price.groupby(pd.Grouper(key='Date', freq='ME'))['Price'].mean()
df_price_monthly.index = df_price_monthly.index.strftime('%Y-%m')

# Output to excel
with pd.ExcelWriter(var.market_price_output + 'toronto_price_time_series_data.xlsx') as writer:
    df_price.to_excel(writer, sheet_name='raw data', index = False)
    df_price_daily.to_excel(writer, sheet_name='daily average')
    df_price_monthly.to_excel(writer, sheet_name='monthly average')
# print(df_price)
