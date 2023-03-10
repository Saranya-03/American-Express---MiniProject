# -*- coding: utf-8 -*-
"""american-express-mini-project (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l6Gcl0cP9UVN-9xxUaYfiPkAd2JwGzeD
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

number_of_transactions = 2
data = pd.read_feather('../input/amexfeather/train_data.ftr').groupby('customer_ID').tail(number_of_transactions).set_index('customer_ID', drop=True).sort_index()
labels = pd.read_csv("../input/amex-default-prediction/train_labels.csv").set_index('customer_ID', drop=True).sort_index()
test_df = pd.read_feather('../input/amexfeather/test_data.ftr').groupby('customer_ID').tail(number_of_transactions).set_index('customer_ID', drop=True).sort_index()

"""**Merge Data**"""

train_df = pd.merge(data, labels, left_index=True, right_index=True) 
print(train_df)
train_df = train_df.drop(["S_2"],axis=1)
test_df = test_df.drop(["S_2"],axis=1)

"""**Preprocessing Data**"""

#Dropping the Transaction Dates
#drop_cols = ['S_2'] 
#train_df.drop(drop_cols, inplace=True, axis=1)

print(train_df.columns)
y = train_df.iloc[:, -1].values


def preprocessing_data(data_x):
    
    # convert categorical variables
    data_x1 = pd.get_dummies(data_x)
    print(data_x1.columns)
    
    print(data_x1)

    #Handling missing values
    col_names = data_x1.columns
    imputer = SimpleImputer()
    data_x1 = pd.DataFrame(imputer.fit_transform(data_x1))  
    data_x1.columns = col_names
    
    # Standardization
    scaler = StandardScaler()
    data_x1 = pd.DataFrame(scaler.fit_transform(data_x1), index=data_x1.index, columns=data_x1.columns)
    return data_x1


x_temp = train_df.iloc[:, :-1]
x=preprocessing_data(x_temp)
test_x = preprocessing_data(test_df)

# Splitting into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size = 0.2, random_state = 0)

"""**Training the Logistic Regression model on the Training set**"""

from sklearn.linear_model import LogisticRegression
logistic_classifier = LogisticRegression(random_state = 0)
logistic_classifier.fit(x_train, y_train)

y_pred_LR = logistic_classifier.predict(x_val)
print(np.concatenate((y_pred_LR.reshape(len(y_pred_LR),1), y_val.reshape(len(y_val),1)),1))

"""**Making the Confusion Matrix of Logistic Regression model**"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm_LR = confusion_matrix(y_val, y_pred_LR)
print(cm_LR)
accuracy_score(y_val, y_pred_LR)

"""**Training the KNN model on the Training set**"""

#from sklearn.neighbors import KNeighborsClassifier
#kNNclassifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
#kNNclassifier.fit(x_train, y_train)

#y_pred_KNN = kNNclassifier.predict(x_val)
#print(y)
#print(y_pred_KNN)
#print(y_val)
#print(np.concatenate((y_pred_KNN.reshape(len(y_pred_KNN),1), y_val.reshape(len(y_val),1)),1))

"""**Making the Confusion Matrix of KNN model**"""

#from sklearn.metrics import confusion_matrix, accuracy_score
#cm_KNN = confusion_matrix(y_val, y_pred_KNN)
#print(cm_KNN)
#accuracy_score(y_val, y_pred_KNN)

"""**Training the SVM model on the Training set**"""

#from sklearn.svm import SVC
#svmclassifier = SVC(kernel = 'linear', random_state = 0)
#svmclassifier.fit(x_train, y_train)

#y_pred_svm = svmclassifier.predict(x_val)
#print(np.concatenate((y_pred_svm.reshape(len(y_pred_svm),1), y_val.reshape(len(y_val),1)),1))

"""**Making the Confusion Matrix of SVM model**"""

#from sklearn.metrics import confusion_matrix, accuracy_score
#cm_svm = confusion_matrix(y_val, y_pred_svm)
#print(cm_svm)
#accuracy_score(y_val, y_pred_svm)

"""**Training XGBoost on the Training set**"""

from xgboost import XGBClassifier
xgb_classifier = XGBClassifier()
xgb_classifier.fit(x_train, y_train)

y_pred_xgb = xgb_classifier.predict(x_val)
print(np.concatenate((y_pred_xgb.reshape(len(y_pred_xgb),1), y_val.reshape(len(y_val),1)),1))

"""**Making the Confusion Matrix of XGB**"""

cm_XGB = confusion_matrix(y_val, y_pred_xgb)
print(cm_XGB)
accuracy_score(y_val, y_pred_xgb)

"""**Handling Test Data**"""

# Loading dataset test_data.csv
#test = pd.read_csv('../input/amex-default-prediction/test_data.csv').groupby('customer_ID').tail(1).set_index('customer_ID')

#test = pd.read_feather('../input/amexfeather/test_data.ftr').groupby('customer_ID').tail(number_of_transactions).set_index('customer_ID', drop=True).sort_index()

#test = pd.read_csv('../input/amex-default-prediction/test_data.csv').groupby('customer_ID').tail(number_of_transactions).set_index('customer_ID', drop=True).sort_index()
print(test_x)

predicted_test_data = xgb_classifier.predict(test_x)
print(predicted_test_data)

output = pd.DataFrame({'customer_ID': test_x.index,'prediction': predicted_test_data})
output.to_csv('submission.csv', index=False, header=True)
