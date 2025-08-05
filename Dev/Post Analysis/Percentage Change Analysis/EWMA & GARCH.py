import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import reduce
import warnings
import re
import openpyxl
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys


project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(project_root)
# print(sys.path)
sys.path.append(project_root)

from utilities import variables as var

df_all_field = pd.read_excel(var.anaylsis_output + 'all_field_data_monthly.xlsx', sheet_name = 'All Data Fields % Change')  # Change this to the actual filename
field_lst = [
    var.toront_demand,
    var.ontario_demand,
    var.toronto_price,	
    var.toronto_temp,
    var.toronto_humidity,
    var.toronto_dew_point,
    var.toronto_wing_speed,
    var.toronto_sea_level_pressure, 
    var.toronto_precipitation
]

df_all_field = df_all_field[['Date'] + field_lst]
df_all_field = df_all_field.drop(0)

final_df_lst = []

for field in field_lst:
    df_field = pd.DataFrame()
    df_field['Date'] = df_all_field['Date']

    ### --- EWMA ---
    # Parameters
    lambda_ = 0.94

    # Initialize variance list
    ewma_variance = [df_all_field[field].iloc[0]**2]

    # Calculate EWMA variance
    for i in range(1, len(df_all_field)):
        prev_var = ewma_variance[-1]
        new_var = lambda_ * prev_var + (1 - lambda_) * df_all_field[field].iloc[i - 1] ** 2
        ewma_variance.append(new_var)
    
    df_field['EWMA_Variance'] = ewma_variance
    df_field['EWMA_StdDev'] = np.sqrt(df_field['EWMA_Variance'])
    

    ### --- GARCH WMA ---
    # Parameters
    gamma = 0.05
    alpha = 0.05
    beta = 0.90

    # Long-run variance: sample variance of the returns
    V_L = df_all_field[field].var()

    # Initialize GARCH variance list
    garch_variance = [df_all_field[field].iloc[0]**2]

    # Compute GARCH(1,1) variance recursively
    for i in range(1, len(df_all_field)):
        prev_var = garch_variance[-1]
        prev_return_sq = df_all_field[field].iloc[i - 1] ** 2
        new_var = gamma * V_L + alpha * prev_return_sq + beta * prev_var
        garch_variance.append(new_var)

    df_field['GARCH_Variance'] = garch_variance
    df_field['GARCH_StdDev'] = np.sqrt(df_field['GARCH_Variance'])



    # saving field df
    final_df_lst.append(df_field)

with pd.ExcelWriter(var.percentage_cgt_output + 'EWMA & GARCH.xlsx') as writer:
    for field, df in zip(field_lst, final_df_lst):
        df.to_excel(writer, sheet_name = field, index = False)

wb = openpyxl.load_workbook(var.percentage_cgt_output + 'EWMA & GARCH.xlsx')

for idx, (sheet, df) in enumerate(zip(wb.worksheets, final_df_lst)):
    # Plot and save image with unique filename
    plt.figure(figsize=(14, 6))
    plt.plot(df['Date'], df['EWMA_StdDev'], label='EWMA', color='blue')
    plt.plot(df['Date'], df['GARCH_StdDev'], label='GARCH', color='red')
    plt.title('EWMA vs. GARCH Estimated Volatility')
    plt.xlabel('Date')
    plt.ylabel('Standard Deviation (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    img_path = f"myplot_{idx}.png"
    plt.savefig(img_path, dpi=100)
    plt.clf()

    img = Image(img_path)
    img.anchor = 'G1'
    sheet.add_image(img)

wb.save(var.percentage_cgt_output + 'EWMA & GARCH_with_img.xlsx')

# removing temperory image files
for idx in range(len(final_df_lst)):
    os.remove(f"myplot_{idx}.png")
    


