'''
多重线性回归/Multiple Linear Regression

Predict MPG with Multiple Linear Regression
X = Weight、Horsepower、Model Year
y = MPG
'''


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib_inline


url = 'AI/DL/mpg.csv'
data = pd.read_csv(url)
print('check 5 randomdata:', data.sample(5))
print('data description:', data.describe())

#clean data
data = data.dropna(subset=['horsepower'])

# check the correlation between features
cols = ['mpg', 'weight', 'horsepower', 'model_year']
print('correlation between features:\n', data[cols].corr())


#visualize the features correlation 
axes = pd.plotting.scatter_matrix(data[cols],alpha=0.2)
plt.tight_layout()
plt.gcf().subplots_adjust(wspace=0, hspace=0)
plt.show()


#select features 
x = data.iloc[:,[3,4,6]].to_numpy()
y = data.iloc[:,[0]].to_numpy()

#Feature Standardization
from sklearn import preprocessing

std_scaler = preprocessing.StandardScaler()
x_std = std_scaler.fit_transform(x)

STD = pd.DataFrame(x_std).describe().round(2)
print(STD)


#Create train and test datasets
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(x_std,y,test_size=0.2,random_state=42)


#Build a multiple linear regression model
from sklearn import linear_model

regressor = linear_model.LinearRegression()
regressor.fit(X_train,y_train)

coef_ = regressor.coef_
intercept_ = regressor.intercept_


