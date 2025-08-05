
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import re
import openpyxl
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys

base_root = 'C:\\Users\\CGOD\\Desktop\\University\\ROP\\IESO MRP Data\\'
sys.path.append(base_root)

from utilities import variables as var


df_precipitation = pd.read_csv(
    var.monthly_precipitation_root + 'grid_TORONTO_line_precip_combined_monthly.csv')

# Transpose all the hour columns
df_precipitation_cleaned = df_precipitation.melt(
    id_vars=['Year'],
    var_name='Month',
    value_name='Millimeter'
)

# Yearly average
df_precipitation_yearly_avg = df_precipitation_cleaned.groupby(
    'Year')['Millimeter'].mean().reset_index()


# Output to excel
with pd.ExcelWriter(var.monthly_precipitation_root + 'cleaned_precipitation.xlsx') as writer:
    df_precipitation_cleaned.to_excel(writer, sheet_name='cleaned raw data', index=False)

    df_precipitation_yearly_avg.to_excel(writer, sheet_name='Yearly Average', index=False)
