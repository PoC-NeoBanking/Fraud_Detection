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

print(fraud)