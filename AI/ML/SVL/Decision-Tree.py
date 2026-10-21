import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import metrics

import matplotlib_inline

import warnings
warnings.filterwarnings('ignore')

#load data
path= 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/drug200.csv'
my_data = pd.read_csv(path)
print("data info:\n",my_data.info())
print("missing values:\n",my_data.isnull().sum())


#LabelEncoder from the Scikit-Learn
label_encoder = LabelEncoder()
my_data['Sex'] = label_encoder.fit_transform(my_data['Sex'])
my_data['BP'] = label_encoder.fit_transform(my_data['BP'])
my_data['Cholesterol'] = label_encoder.fit_transform(my_data['Cholesterol'])
print(my_data)


#
custom_map = {'drugA':0,'drugB':1,'drugC':2,'drugD':3,'drugE':4}
my_data['Drug_num'] = my_data['Drug'].map(custom_map)
print(my_data)

#correlation
corr = my_data.drop('Drug',axis=1).corr()['Drug_num']
print(corr)



# Plot the count plot
category_counts = my_data['Drug'].value_counts()
plt.bar(category_counts.index, category_counts.values, color='blue')
plt.xlabel('Drug')
plt.ylabel('Count')
plt.title('Category Distribution')
plt.xticks(rotation=45)  # Rotate labels for better readability if needed
plt.show()

#Modeling
y = my_data['Drug']
X = my_data.drop(['Drug','Drug_num'], axis=1)
X_trainset, X_testset, y_trainset, y_testset = train_test_split(X, y, test_size=0.3, random_state=42)
drugTree = DecisionTreeClassifier(criterion="entropy", max_depth = 4)
drugTree.fit(X_trainset,y_trainset)

#Evaluation
tree_predictions = drugTree.predict(X_testset)
print("Decision Trees's Accuracy: ", metrics.accuracy_score(y_testset, tree_predictions))

#Visualize the tree
plot_tree(drugTree)
plt.show()