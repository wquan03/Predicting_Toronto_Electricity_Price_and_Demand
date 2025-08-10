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

demand_prefix = 'PUB_Demand_'
start_year = 2002
ontario_demand_source_path = var.demand_input + 'Ontario\\'
header = 3

df_demand_final = util.combine_csvs(demand_prefix, start_year, ontario_demand_source_path, header)
df_demand_final.to_csv(ontario_demand_source_path + demand_prefix + 'merged.csv', index = False)