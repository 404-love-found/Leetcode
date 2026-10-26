import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib_inline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/teleCust1000t.csv')
df.info()
Missing_values = df.isnull().sum().sum()
print("Missing_values:",Missing_values)
df['custcat'].value_counts()
 

correlation_matrix = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
correlation_values = abs(df.corr()['custcat'].drop('custcat')).sort_values(ascending=False)
print("Correlation:",correlation_values)
plt.show()

#Data split
X = df.drop('custcat',axis=1)
y = df['custcat']

#Normalize Data
Standscaler = StandardScaler()
X_norm = Standscaler.fit_transform(X)

#Split Train and test data 
X_train,X_test,y_train,y_test = train_test_split(X_norm,y,test_size=0.2,random_state=42)

#KNN Classification
K = 3
knn_classifer = KNeighborsClassifier(n_neighbors=K)
Knn_model = knn_classifer.fit(X_train,y_train)

yhat = knn_classifer.predict(X_test)
print("Test set Accuracy: ", accuracy_score(y_test, yhat))