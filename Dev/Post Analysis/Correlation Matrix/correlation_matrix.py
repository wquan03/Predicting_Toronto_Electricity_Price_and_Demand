import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import re
import openpyxl
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utilities import variables as var



df = pd.read_excel(var.anaylsis_output + 'all_field_data_daily.xlsx', sheet_name = 'All Data Fields')
df = df.drop('Date', axis = 1)

# Drop rows with NA values to ensure clean correlation calculation
df_clean = df.dropna()

# Calculate the correlation matrix
correlation_matrix = df_clean.corr()

# Display the result
print(correlation_matrix)

# Save to Excel
correlation_matrix.to_excel(var.correlation_matrix_output + "correlation_matrix.xlsx")