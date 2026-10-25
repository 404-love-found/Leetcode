'''
Credit Card Fraud Detection with Decision Trees and SVM

Objectives:
Perform basic data preprocessing in Python
Model a classification task using the Scikit-Learn Python APIs
Train Suppport Vector Machine and Decision Tree models using Scikit-Learn
Run inference and assess the quality of the trained models

'''


# Import the libraries we need to use in this lab
from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_inline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score
from sklearn.svm import LinearSVC

import warnings
warnings.filterwarnings('ignore')


#import data
url= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/creditcard.csv"
raw_data = pd.read_csv(url)
print("data information:\n",raw_data.info())


#Data analysis
labels = raw_data.Class.unique() #distinct classes
sizes = raw_data.Class.value_counts().values #count of each class
# plot the class value counts
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.3f%%')
ax.set_title('Target Variable Value Counts')
plt.show()

#check correlation
Correlation_values = raw_data.corr()['Class'].drop('Class') 
Correlation_values.plot(kind='barh', figsize=(10, 6))


#Dataset Preprocessing
#=====standardize features by removing the mean and scaling to unit variance=======
raw_data.iloc[:, 1:30] = StandardScaler().fit_transform(raw_data.iloc[:, 1:30])
data_matrix = raw_data.values  
#====X: feature matrix (for this analysis, we exclude the Time variable from the dataset)=====
X = data_matrix[:, 1:30]
#====y: labels vector=======
y = data_matrix[:, 30] 
#====data normalization=======
X = normalize(X, norm="l1")

#Dataset Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Build a Decision Tree Classifier model with Scikit-Learn
w_train = compute_sample_weight('balanced', y_train)
dt = DecisionTreeClassifier(max_depth=4, random_state=35)
dt.fit(X_train, y_train, sample_weight=w_train)

#Build a Support Vector Machine model with Scikit-Learn
SVM =LinearSVC(class_weight='balanced',random_state=42,loss='hinge',fit_intercept=False)
SVM.fit(X,y)


#Evaluate the Decision Tree Classifier Models
y_pred_dt = dt.predict_proba(X_test)[:,1]
roc_auc_dt = roc_auc_score(y_test, y_pred_dt)
print('Decision Tree ROC-AUC score : {0:.3f}'.format(roc_auc_dt))

#Evluate the SVM 
y_pred_svm = SVM.decision_function(X_test)
roc_auc_svm = roc_auc_score(y_test, y_pred_svm)
print("SVM ROC-AUC score: {0:.3f}".format(roc_auc_svm))

