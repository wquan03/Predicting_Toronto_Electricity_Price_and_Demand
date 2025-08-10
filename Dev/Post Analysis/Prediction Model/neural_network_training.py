# --- train_model.py ---
import numpy as np
import pandas as pd
import itertools
import json
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
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
print("The following are my features")
print(X.columns)


# y = df[var.toront_demand].values
y = df[var.toronto_price].values

# Split and scale
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
x_scaler = StandardScaler()
y_scaler = StandardScaler()
X_train_scaled = x_scaler.fit_transform(X_train)
y_train_scaled = y_scaler.fit_transform(y_train.reshape(-1, 1)).ravel()


### --- Defining Hyperparameters ---
# Hyperparameter grid
size_vals = [5, 25, 50, 100, 250]
shapes = (list(itertools.product(size_vals, repeat=1)) +
          list(itertools.product(size_vals, repeat=2)) +
          list(itertools.product(size_vals, repeat=3)) +
          list(itertools.product(size_vals, repeat=4)))

param_grid = {
    'hidden_layer_sizes': shapes,
    'learning_rate': ['constant', 'adaptive', 'invscaling'],
    'batch_size': [4, 8, 16, 32, 64, 128],
    'alpha': [0.1, 0.01, 0.001],
    'activation': ['tanh', 'relu']
}


### --- Training a Neural Network Model ---
# Define model
# model = MLPRegressor(max_iter=10000, solver='adam', random_state=42, verbose=True)

model = MLPRegressor(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    alpha=0.001,
    learning_rate='adaptive',
    batch_size=32,
    solver='adam',
    max_iter=10000,
    random_state=42
)

# Hyperparameter search
searcher = RandomizedSearchCV(model, param_distributions=param_grid, scoring='r2', n_iter=20, cv=3, n_jobs=-1, verbose=3)
# searcher = RandomizedSearchCV(estimator=model, n_jobs=-1, cv=3, param_distributions=param_grid, scoring="r2", verbose=3)
searchResults = searcher.fit(X_train_scaled, y_train_scaled)

# Save best parameters
best_params = searchResults.best_params_
with open(var.model_output + "best_nn_params_for_price.json", "w") as f:
# with open(var.model_output + "best_nn_params_for_demand.json", "w") as f:
    json.dump(best_params, f, indent=4)

print("Best Parameters Saved:", best_params)
