import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


#read in the data using pandas
daily_file_nm = 'all_field_data_daily'
df = pd.read_csv(daily_file_nm + '_with_outlier.csv')

#create a dataframe with all training data except the target column
df = df.drop('Date', axis = 1)
X = df.drop(columns=['Price is spike', 'Toronto Demand is spike'])

#separate target values
y = df['Price is spike'].values
# y2 = df['Toronto Demand is spike'].values

# Combine targets into a 2D array
# y = np.column_stack((y1, y2))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1, stratify=y)

clf = LogisticRegression(max_iter=10000, random_state=1)
# multi_target_clf = MultiOutputClassifier(estimator = clf)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

count = 0
for i, j in zip(y_test, y_pred):
    if i == j:
        count += 1
        
print(count)
print(count / len(y_test))


y_test_df = pd.DataFrame(
    data = {
        'target1': y_test
    }
)
y_pred_df = pd.DataFrame(
    data = {
        'pred_target1': y_pred
    }
)
X_test_df = X_test.reset_index(drop = True)
temp = pd.concat([X_test_df, y_test_df, y_pred_df], axis = 1)
temp.to_csv('temp.csv', index = False)
print(temp.head())

acc = accuracy_score(y_test, y_pred) * 100
print(f"Logistic Regression model accuracy: {acc:.2f}%")