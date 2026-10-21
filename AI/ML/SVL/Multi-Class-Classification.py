import numpy as np                                      # 数组工具，别名 np
import pandas as pd                                     # 表格工具，别名 pd
import matplotlib.pyplot as plt                         # 画图工具，别名 plt
import seaborn as sns                                   # 更好看的统计图工具，别名 sns
from sklearn.model_selection import train_test_split    # 划分训练/测试集的函数
from sklearn.linear_model import LogisticRegression     # 逻辑回归模型（类）
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier  # 两种"把二分类变多分类"的包装器（类）
from sklearn.preprocessing import StandardScaler, OneHotEncoder         # 标准化、独热编码工具（类）
from sklearn.metrics import accuracy_score              # 准确率函数
import warnings
warnings.filterwarnings('ignore')   

import warnings
warnings.filterwarnings('ignore')



#-----------1.load data-----------
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/GkDzb7bWrtvGXdPOfk6CIg/Obesity-level-prediction-dataset.csv"
data = pd.read_csv(url)
print("head:\n",data.head())

#-----------2.Distribution of target variable-----------
sns.countplot(y ='NObeyesdad',data = data)
plt.title('Distribution of Obesity Levels')
plt.show()

#------------3.Data Preprocessing--------------
continuous_columns = data.select_dtypes(include=['float64']).columns.tolist()  # 所有小数列的列名 → list
scaler = StandardScaler()                               # 建一个标准化工具（还没学任何东西）
scaled_features = scaler.fit_transform(data[continuous_columns])  # 学均值/标准差 + 变换，返回 ndarray (2111, 8)
scaled_df = pd.DataFrame(scaled_features, columns=scaler.get_feature_names_out(continuous_columns))  # 变回带列名的表
scaled_data = pd.concat([data.drop(columns=continuous_columns), scaled_df], axis=1)  # 去掉旧数字列，左右拼上新数字列


#-------------4.one-hot encoder----------
categorical_columns = scaled_data.select_dtypes(include=['object']).columns.tolist()  # 所有文字列的列名
categorical_columns.remove('NObeyesdad')                # 目标列不编码，从 list 里删掉（直接改原 list）
encoder = OneHotEncoder(sparse_output=False, drop='first')  # 输出普通数组；每个特征丢掉第一个类别
encoded_features = encoder.fit_transform(scaled_data[categorical_columns])  # ndarray (2111, 15)
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_columns))
prepped_data = pd.concat([scaled_data.drop(columns=categorical_columns), encoded_df], axis=1)  # (2111, 24)


prepped_data['NObeyesdad'] = prepped_data['NObeyesdad'].astype('category').cat.codes
print(prepped_data.head())

#--------------5.train/test---------
X = prepped_data.drop('NObeyesdad',axis=1)
y = prepped_data['NObeyesdad']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

#-------------6.ONE vs ALL----------
model_ova = OneVsRestClassifier(LogisticRegression(max_iter=1000))
model_ova.fit(X_train,y_train)
y_pred_ova = model_ova.predict(X_test)
print("One-vs-All (OvA) Strategy")
print(f"Accuracy: {np.round(100*accuracy_score(y_test, y_pred_ova), 2)}%")


#-------------7.ONE vs ONE-----------
model_ovo = OneVsOneClassifier(LogisticRegression(max_iter=1000))
model_ovo.fit(X_train,y_train)
y_pred_ovo = model_ovo.predict(X_test)
print("One-vs-One (OvO) Strategy")
print(f"Accuracy: {np.round(100*accuracy_score(y_test, y_pred_ovo), 2)}%")
