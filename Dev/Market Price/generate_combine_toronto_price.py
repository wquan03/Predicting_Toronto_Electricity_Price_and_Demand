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
from utilities import utililty as util

price_prefix = 'PUB_PriceNodal_'
start_year = 2002
nodal_price_source_path = var.market_price_input + 'Nodal Price\\'
header = 4

df_price_final = util.combine_csvs(price_prefix, start_year, nodal_price_source_path, header)
df_price_final = df_price_final[['Date', 'Hour', 'Darlington']]

# Combining date with hour
df_price_final['Date'] = pd.to_datetime(df_price_final['Date'])
df_price_final['Date'] = df_price_final['Date'] + pd.to_timedelta(df_price_final['Hour'], unit='h')
df_price_final = df_price_final.drop('Hour', axis = 1)

with pd.ExcelWriter(nodal_price_source_path + price_prefix + 'merged.xlsx') as writer:
    df_price_final.to_excel(writer, index = False)