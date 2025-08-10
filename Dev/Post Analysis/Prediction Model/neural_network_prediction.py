import numpy as np
import pandas as pd
import json
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from utilities import variables as var

### --- Data Input --- 
df = pd.read_excel(var.anaylsis_output + 'all_field_data_daily.xlsx', sheet_name='All Data Fields')


### --- Data Preprocessing --- 
# Define features
feature_lst = df.columns.tolist()
feature_lst.remove(var.toront_demand)
feature_lst.remove(var.toronto_price)
feature_lst.remove(var.ontario_demand)
feature_lst.remove('Date')

# feature_lst = [var.ontario_supply, var.toronto_temp, var.gas_price, var.month]
df = df[[var.toront_demand, var.toronto_price] + feature_lst]

# Create X and y
X = df.drop(columns=[var.toronto_price, var.toront_demand])
y = df[var.toront_demand].values
# y = df[var.toronto_price].values

# Scale data
x_scaler = StandardScaler()
y_scaler = StandardScaler()
X_scaled = x_scaler.fit_transform(X)
y_scaled = y_scaler.fit_transform(y.reshape(-1, 1)).ravel()

# Split data
X_train_scale, X_test_scale, y_train_scale, y_test_scale = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
# y_train_scale_scaled = y_scaler.transform(y_train_scale.reshape(-1, 1)).ravel()
# y_test_scale_scaled = y_scaler.transform(y_test_scale.reshape(-1, 1)).ravel()


### --- Defining the Model Based on Trained Results ---
# Load best parameters
# with open(var.model_output + "best_nn_params_for_price.json", "r") as f:
with open(var.model_output + "best_nn_params_for_demand.json", "r") as f:
    best_params = json.load(f)

# Rebuild and train model
model = MLPRegressor(**best_params, max_iter=10000, solver='adam', random_state=42)
model.fit(X_train_scale, y_train_scale)

# Predict
y_pred_scaled = model.predict(X_test_scale)

# Evaluate
y_pred = y_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
y_test = y_scaler.inverse_transform(y_test_scale.reshape(-1, 1)).ravel()
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Loaded Model MSE: {mse:.2f}, R2: {r2:.2f}")

### --- Prediction ---
predict_data = [15707.64651, 5.32, 11.71, 84.8, 9.1, 15.62, 100.98, 4.4, 0.6, 4.8, 0, 7.4, 2003, 5, 1, 3, 0, 137.1241, 0, 4861000]
# predict_data = [15707.64651, 11.71, 5.32, 5]
# print(len(predict_data))
# print(len(feature_lst))
# print(feature_lst)
predict_df = pd.DataFrame(
    [predict_data], 
    columns = feature_lst
)

# Scale the predicting features
predict_df_scaled = x_scaler.transform(predict_df)

# Predict using the trainned model
predicted_value_scaled = model.predict(predict_df_scaled)

# Inverse transform to get real-world demand value
predicted_value = y_scaler.inverse_transform(
    predicted_value_scaled.reshape(-1, 1)
).ravel()[0]


print('Prediction Input Data: ' + str(predict_data))
print(f"Prediction for new data: {predicted_value}")

# errors = y_test - y_pred
# plt.hist(errors, bins=50)
# plt.title("Prediction Errors")
# plt.xlabel("Error (MW)")
# plt.ylabel("Frequency")
# plt.grid(True)
# plt.show()




plt.scatter(y_test, y_pred, alpha=0.4)
plt.xlabel("Actual Demand (MW)")
plt.ylabel("Predicted Demand (MW)")
plt.title("Actual vs. Predicted Toronto Demand")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
plt.grid(True)
plt.show()
