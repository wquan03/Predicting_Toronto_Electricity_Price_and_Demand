import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import numpy as np



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


#split dataset into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)


print('First KNN: ')
# Create KNN classifier
knn = KNeighborsClassifier(n_neighbors = 3)
# Wrap KNN with MultiOutputClassifier
# multi_target_knn = MultiOutputClassifier(estimator = knn)
# Fit the model
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

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

#check accuracy of our model on the test data
print(knn.score(X_test, y_test))
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print()


# print('KNN with CV:')
# #create a new KNN model
# knn_cv = KNeighborsClassifier(n_neighbors=3)
# multi_target_knn_cv = MultiOutputClassifier(estimator = knn_cv)
# #train model with cv of 5 
# cv_scores = cross_val_score(multi_target_knn_cv, X, y, cv=5)
# #print each cv score (accuracy) and average them
# print(cv_scores)
# print('cv_scores mean:{}'.format(np.mean(cv_scores)))
# print()

# print('KNN with grid search')
# #create new a knn model
# knn2 = KNeighborsClassifier()
# multi_target_knn_2 = MultiOutputClassifier(estimator = knn2)
# #create a dictionary of all values we want to test for n_neighbors
# param_grid = {'n_neighbors': np.arange(1, 25)}
# #use gridsearch to test all values for n_neighbors
# knn_gscv = GridSearchCV(knn2, param_grid, cv=5)
# #fit model to data
# knn_gscv.fit(X, y)
# print(knn_gscv.best_params_)
# print(knn_gscv.best_score_)