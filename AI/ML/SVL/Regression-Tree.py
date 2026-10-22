#Obejctives:predict the amount of tip paid
from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_inline

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.metrics import mean_squared_error

import warnings
warnings.filterwarnings('ignore')

#====load data==========
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/pu9kbeSaAtRZ7RxdJKX9_A/yellow-tripdata.csv'
raw_data = pd.read_csv(url)

print("data info:\n",raw_data.info())
print("missing values:\n",raw_data.isnull().sum())


#=====2.Correlation========
correlation_values = raw_data.corr(numeric_only=True)['tip_amount'].drop('tip_amount')
correlation_values = correlation_values.sort_values()
print(correlation_values) 

#======3.plot the correlation===
ax = correlation_values.plot(kind='barh', figsize=(10, 6))   
ax.set_title('Correlation with tip_amount')                 
ax.set_xlabel('correlation')                                 
plt.tight_layout()                   
plt.show()                           

#====4.Data preprocess======
y = raw_data[['tip_amount']].values.astype('float32')
proc_data = raw_data.drop(['tip_amount'],axis=1)
X = proc_data.values
X = normalize(X, axis=1, norm='l1', copy=False)

#====5.Split the data======
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("X_train:", X_train.shape, " X_test:", X_test.shape)   
print("y_train:", y_train.shape, " y_test:", y_test.shape)

#====5.Build the model=====
from sklearn.tree import DecisionTreeRegressor 
DT_reg = DecisionTreeRegressor(criterion='squared_error',max_depth=6,random_state=42)
DT_reg.fit(X_train, y_train)

#===6.Predict ====
y_pred = DT_reg.predict(X_test)
mse_score = mean_squared_error(y_test, y_pred)          
print('MSE score : {0:.3f}\n'.format(mse_score))

r2 = DT_reg.score(X_test, y_test)                        
print('R^2 score : {0:.3f}\n'.format(r2)) 