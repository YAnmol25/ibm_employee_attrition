# -*- coding: utf-8 -*-
"""IBM_Employee_Attrition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wZKlIuzZHSlxy9Ubt84JvusaEEEXGQzR
"""

#Description: This program predicts employee attrition

#Import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Load the data
from google.colab import files
files.upload()

#Store the data in a data frame
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')


#Print the first 7 rows of the data
df.head(7)

#Get the no of rows and columns
df.shape

#Get the column data type
df.dtypes

#Get a count of the empty values for each column
df.isna().sum()

#Check for any missing / null values in data set
df.isnull().values.any()

#View some statistics
df.describe()

#Get a count of the no of employees that stayed and left the company
df['Attrition'].value_counts()

#Visualize the number of employees that stayed and left the company 
sns.countplot(df['Attrition'])

#Show the nuumber of employees that stayed and left by age
plt.subplots(figsize=(12,4))
sns.countplot(x='Age', hue='Attrition', data=df, palette='colorblind')

#Print all of the data types and their unique values
for column in df.columns:
  if df[column].dtype == object:
    print(str(column) + ' : '+ str(df[column].unique()))
    print(df[column].value_counts())
    print('_________________________________________________________')

#Remove some useless columns
df = df.drop('Over18', axis= 1)
df = df.drop('EmployeeNumber', axis= 1)
df = df.drop('StandardHours', axis= 1)
df = df.drop('EmployeeCount', axis= 1)

#Get the correlation
df.corr()

#Visualize the correlation
plt.figure(figsize=(15,15))
sns.heatmap(df.corr(), annot=True, fmt= '.0%')

#Transform the data
#Transform non-numerical into numeric column
from sklearn.preprocessing import LabelEncoder

for column in df.columns:
  if df[column].dtype == np.number:
        continue
  df[column] = LabelEncoder().fit_transform(df[column])

"""Age column is at 1st place we need Attrition at 1st so creating new column and then drop to make Attrition 1st column to make splitting the data easier."""

#Create a new column 
df['Age_years'] = df['Age']

#Drop the age column
df = df.drop('Age', axis=1)

df

#Split the data 
X = df.iloc[:, 1:df.shape[1]].values
Y = df.iloc[:, 0].values

#Split the data into 75% training and 25% testing 
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.2, random_state= 0)

#USe the Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators= 10, criterion= 'entropy', random_state= 0)
forest.fit(X_train,Y_train)

#Get the accuracy on traing data set
forest.score(X_train,Y_train)

#Show the confusion metrix and accuracy score for the model on the test data
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(Y_test, forest.predict(X_test))

TN = cm[0][0]
TP = cm[1][1]
FN = cm[1][0]
FP = cm[0][1]

print(cm)
print('Model Testing Accuracy = {}'.format( (TP + TN ) / (TP + TN + FN + FP) ))

#Get the precision, recall and f1-score
from sklearn.metrics import classification_report

print( classification_report(Y_test, forest.predict(X_test)))