from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd



#read in the data using pandas
daily_file_nm = 'all_field_data_daily'
df = pd.read_csv(daily_file_nm + '_with_outlier.csv')

#create a dataframe with all training data except the target column
df = df.drop('Date', axis = 1)
X = df.drop(columns=['Price is spike', 'Toronto Demand is spike'])

# creating feature variables
y = df['Price is spike'].values

# creating train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


mlp = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=10000, random_state=42)
mlp.fit(X_train, y_train)



# prediction
y_pred = mlp.predict(X_test)

count = 0
one_count = 0
for i, j in zip(y_test, y_pred):
    if j == 1:
        one_count += 1
    if i == j:
        count += 1
        
print(count, one_count)
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
# X_test_df = X_test.reset_index(drop = True)
temp = pd.concat([y_test_df, y_pred_df], axis = 1)
temp.to_csv('temp.csv', index = False)


acc = accuracy_score(y_test, y_pred) * 100
print(f"Logistic Regression model accuracy: {acc:.2f}%")

class_report = classification_report(y_test, y_pred)
print("Classification Report:\n", class_report)