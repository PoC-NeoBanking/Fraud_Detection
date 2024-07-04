import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# loading the dataset to a Pandas DataFrame
transaction_data = pd.read_csv('train_trans.csv')

# separating the data for analysis
legit = transaction_data[transaction_data.detected_fraud == False]
fraud = transaction_data[transaction_data.detected_fraud == True]

legit_sample = legit.sample(n=21)
new_dataset = pd.concat([legit_sample, fraud], axis=0)
new_dataset['transaction_date'] = pd.to_datetime(new_dataset['transaction_date']).astype(np.int64)


X = new_dataset.drop(columns='transaction_category', axis=1)
Y = new_dataset['detected_fraud']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)
print(X)

print(Y)
model = LogisticRegression()

model.fit(X_train, Y_train)

# accuracy on training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('Accuracy on Training data : ', training_data_accuracy)

# accuracy on test data
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print('Accuracy score on Test Data : ', test_data_accuracy)
