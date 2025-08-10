# importing modules and packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
from sklearn.metrics import accuracy_score

#read in the data using pandas
daily_file_nm = 'all_field_data_daily'
df = pd.read_excel(daily_file_nm + '.xlsx', sheet_name = 'All Data Fields')

#create a dataframe with all training data except the target column
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df = df.drop(['Date', 'Ontario Demand'], axis = 1)
X = df.drop(columns=['Price', 'Toronto Demand'])

# creating feature variables
y = df['Price'].values
# y = df['Toronto Demand'].values

# creating train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# creating a regression model
model = LinearRegression()

# tune the hyper parameters
param_space = {
    'copy_X': [True,False], 
    'fit_intercept': [True,False], 
    'n_jobs': [1,5,10,15,None], 
    'positive': [True,False]
}

grid_search = GridSearchCV(model, param_space, cv=5)
grid_search.fit(X_train, y_train)

print(f"Best Hyperparameters: {grid_search.best_params_}")
model = grid_search.best_estimator_
print(model.get_params())

# 4. Make Predictions on the Test Set
y_pred = model.predict(X_test)

# 5. Evaluate the Model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Coefficients: {model.coef_}")
print(f"Model Intercept: {model.intercept_}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-squared (R2): {r2:.2f}")

# 6. Make a prediction for new data
# Temperature	Relative Humidity	Dew Point	Wind Speed	Sea Level Pressure	HDD 15.5	CDD 15.5	HDD 18	CDD 18	Precipitation (mm)
# 11.71	84.8	9.1	15.62	100.98	4.4	0.6	4.8	0	7.4
# new_data = pd.DataFrame([[11.71, 84.8, 9.1, 15.62, 100.98, 4.4, 0.6, 4.8, 0, 7.4]], columns=['Temperature', 'Relative Humidity', 'Dew Point', 'Wind Speed', 'Sea Level Pressure', 'HDD 15.5', 'CDD 15.5', 'HDD 18', 'CDD 18', 'Precipitation (mm)'])
# predicted_value = model.predict(new_data)
# print(f"Prediction for new data ([11.71, 84.8, 9.1, 15.62, 100.98, 4.4, 0.6, 4.8, 0, 7.4]): {predicted_value[0]:.2f}")