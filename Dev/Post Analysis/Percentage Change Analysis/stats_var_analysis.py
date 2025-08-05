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



df = pd.read_excel(var.anaylsis_root + 'all_field_data_monthly.xlsx', sheet_name = 'All Data Fields % Change')  # Change this to the actual filename
df = df.drop('Date', axis = 1)


df_additional_stats = df.agg(['mean', 'std', 'var', 'skew', 'kurt'])
df_additional_stats = df_additional_stats.T

# Optional: save to Excel
df_additional_stats.to_excel(var.percentage_root + "std_var_skew_kurt.xlsx")