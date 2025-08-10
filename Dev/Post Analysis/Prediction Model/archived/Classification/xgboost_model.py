import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report, average_precision_score
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from utilities import variables as var
from utilities import utililty as util

### --- Data Input --- 
df = pd.read_excel(var.anaylsis_output + 'all_field_data_daily.xlsx', sheet_name = 'All Data Fields')

# Define the features
feature_lst = [var.toronto_temp, var.ontario_supply, var.gas_price, var.month]
df = df[[var.toront_demand, var.toronto_price] + feature_lst]

# calculate outliers for classification
df, price_spike_col_nm = util.cal_outlier_df(df, 'Price')
df, demand_spike_col_nm = util.cal_outlier_df(df, 'Toronto Demand')

X = df.drop(columns=[price_spike_col_nm, demand_spike_col_nm])
print(X.columns)
# creating feature variables
# y = df[price_spike_col_nm].values
y = df[demand_spike_col_nm].values


### --- Data Preprocessing --- 
# spliting the dateset into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)

# Scale numerical features - notes: important for logistic regression and good practice in general
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


### --- Handling Data Imbalance with SMOTE ---
print(' --- Applying SMOTE to the training data --- ')
print()
smote = SMOTE(random_state = 42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
print('Original training shape:', y_train.shape)
print('Resample training shape:', y_train_resampled.shape)


### --- Defining Hyperparameters ---
param_grid = {
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'n_estimators': [100, 200, 300],
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
}


### --- Train an Advance Model (XGBoost) ---
print(' --- Training Advanced Model: XGBoost --- ')
print()
xgb_model = xgb.XGBClassifier(objective = 'binary:logistic', random_state = 42)
# xgb_model = xgb.XGBClassifier(objective = 'binary:logistic', eval_metrix = 'logloss', use_label_encoder = False, random_state = 42)

# tunning hyperparameters
random_search = RandomizedSearchCV(
    estimator = xgb_model,
    param_distributions = param_grid, 
    n_iter = 50,
    scoring = 'f1',
    cv = 3, 
    verbose = 1,
    n_jobs = 1,
    random_state = 42
)
print(' --- Staring to tune hyperparameters --- ')
random_search.fit(X_train_resampled, y_train_resampled)
best_xgb_model = random_search.best_estimator_
print(' --- tuning complete --- ')
print()
print('Best Parameters Found: ')
print(random_search.best_params_)

y_pred_xgb = best_xgb_model.predict(X_test_scaled)
print()
print('XGBoost Classification Report: ')
print(classification_report(y_test, y_pred_xgb))
print(f'XGBoost F1-Score: {f1_score(y_test, y_pred_xgb):.4f}')
print()

