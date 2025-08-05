import pandas as pd
import os


base_root = 'C:\\Users\\CGOD\\Desktop\\University\\ROP\\IESO MRP Data\\'
base_input = base_root + 'Input & Output\\Input\\'
base_output = base_root + 'Input & Output\\Output\\'

demand_input = base_input + 'Demand\\'
demand_output = base_output + 'Demand\\'

supply_input = base_input + 'Supply\\'
supply_output = base_output + 'Supply\\'

supply_canada_stats = supply_input + 'Canada Stats\\'

market_price_input = base_input + 'Market Price\\'
market_price_output = base_output + 'Market Price\\'
gas_price_input = market_price_input + 'Gas and Carbon\\'

anaylsis_input = base_input + 'Post Analysis\\'
anaylsis_output = base_output + 'Post Analysis\\'

correlation_matrix_input = anaylsis_input + 'Correlation Matrix\\'
correlation_matrix_output = anaylsis_output + 'Correlation Matrix\\'

percentage_cgt_input = anaylsis_input + 'Percentage Change Analysis\\'
percentage_cgt_output = anaylsis_output + 'Percentage Change Analysis\\'

model_input = anaylsis_input + 'Prediction Model\\'
model_output = anaylsis_output + 'Prediction Model\\'



weather_input = base_input + 'Weather\\'
weather_output = base_output + 'Weather\\'

population_input = base_input + 'Population\\'


cur_year = 2025

year = 'Year'
month = 'Month'
day = 'Day'
toront_demand = 'Toronto Demand'	
ontario_demand = 'Ontario Demand'
ontario_supply = 'MW Amount'
toronto_price = 'Price'	
gas_price = 'Gas Price'
toronto_temp = 'Temperature'
toronto_humidity = 'Relative Humidity'
toronto_dew_point = 'Dew Point'
toronto_wing_speed = 'Wind Speed'
toronto_sea_level_pressure = 'Sea Level Pressure'
toronto_precipitation = 'Precipitation (mm)'
hdd_15 = 'HDD 15.5'
cdd_15 = 'CDD 15.5'
hdd_18 = 'HDD 18'
cdd_18 = 'CDD 18'	
population = 'Population'


model_field_lst = [
    ontario_demand,
    toronto_price,	
    toronto_temp,
    toronto_humidity,
    toronto_dew_point,
    toronto_wing_speed,
    toronto_sea_level_pressure, 
    toronto_precipitation,
    hdd_15,
    cdd_15,
    hdd_18,
    cdd_18
]










