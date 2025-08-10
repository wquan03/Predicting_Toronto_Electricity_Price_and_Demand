import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow as tf
import os



# 1. Generate synthetic data for regression
daily_file_nm = 'all_field_data_daily'
df = pd.read_excel(daily_file_nm + '.xlsx', sheet_name = 'All Data Fields')

#create a dataframe with all training data except the target column
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

df_population = pd.read_excel('toronto_yearly_population.xlsx')
df = df.merge(df_population, how = 'left', on = 'Year')

# df = df.drop(['Date', 'Ontario Demand'], axis = 1)
df = df.drop(['Date', 'Ontario Demand', 'HDD 15.5', 'CDD 15.5', 'HDD 18', 'CDD 18'], axis = 1)

X = df.drop(columns=['Price', 'Toronto Demand'])

# creating feature variables
y = df['Price'].values
# y = df['Toronto Demand'].values

test_split = int(len(df) * 0.8)
train_df, test_df = df[1:test_split], df[test_split:] 

train = train_df
scalers={}
for i in train_df.columns:
    scaler = MinMaxScaler(feature_range=(-1,1))
    s_s = scaler.fit_transform(train[i].values.reshape(-1,1))
    s_s=np.reshape(s_s,len(s_s))
    scalers['scaler_'+ i] = scaler
    train[i]=s_s
test = test_df
for i in train_df.columns:
    scaler = scalers['scaler_'+i]
    s_s = scaler.transform(test[i].values.reshape(-1,1))
    s_s=np.reshape(s_s,len(s_s))
    scalers['scaler_'+i] = scaler
    test[i]=s_s