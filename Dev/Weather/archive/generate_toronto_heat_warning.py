import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import re
import openpyxl
import json
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utilities import variables as var

with open(var.weather_input + 'heat-alert-data-json.json', 'r') as f:
    data = json.load(f)


date = []
code = []
for warning in data:
    print(warning)
    date.append(warning.get('date'))
    code.append(warning.get('code'))