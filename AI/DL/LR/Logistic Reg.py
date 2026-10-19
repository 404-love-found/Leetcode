import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import log_loss
import matplotlib.pyplot as plt

import matplotlib_inline

import warnings
warnings.filterwarnings('ignore')


#Load Data from URL
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/ChurnData.csv"
churn_pd = pd.read_csv(url)

#check the data
print("info:\n",churn_pd.info())
print("first five data:\n",churn_pd.sample(5))
print("describe:\n",churn_pd.describe())

#Data Preprocessing
churn_pd = churn_pd[['tenure', 'age', 'address', 'income', 'ed', 'employ', 'equip', 'churn']]
churn_pd['churn'] = churn_pd['churn'].astype('int')

print("Data:\n",churn_pd)

X = np.asarray(churn_pd[['tenure', 'age', 'address', 'income', 'ed', 'employ', 'equip']])
y = np.asarray(churn_pd[['churn']])

#standardize dataset in order to have all the features at the same scale
X_norm = StandardScaler().fit(X).transform(X)


#Splitting the dataset
X_train,X_test,y_train,y_test = train_test_split(X_norm,y,test_size=0.2,random_state=42)

#Logistic Regression Classifier modeling
LR = LogisticRegression().fit(X_train,y_train)

yhat = LR.predict(X_test)
print("predict the output variable:\n",yhat)
#prediction probability of data point of the test data set
yhat_prob = LR.predict_proba(X_test)
print("prediction probability:\n",yhat_prob)

coeffecients = pd.Series(LR.coef_[0],index=churn_pd.columns[:-1])
coeffecients.sort_values().plot(kind='barh')
plt.title("Feature Coefficients in Logistic Regression Churn Model")
plt.xlabel("Coefficient Value")
plt.show()

#Performance Evaluation
ll = log_loss(y_test,yhat_prob)
print("log_loss:",ll)

