'''
线性回归训练,机器学习Linear Regression Training, Machine Learning
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib_inline

#载入数据
# 1. 自动获取 LR.py 所在目录 (AI/DL/) 下的 mpg.csv 路径
url = 'AI/DL/mpg.csv'
data = pd.read_csv(url)
#检测数据
print('随机查看5条数据:', data.sample(5))

describe = data.describe()  # 查看数据的基本统计信息
print('数据的基本统计信息:', describe)


#特征筛选（提取子表）并随机抽样预览
cdf = data[['mpg','weight']]
print('特征筛选后的数据:', cdf.sample(5))


'''
根据车身重量 (weight) 来预测 燃油效率 (mpg)
练习步骤要求
特征提取：从 df 中提取核心子表 cdf = df[['weight', 'mpg']]，
使用训练好的模型预测：如果一辆新车的重量为 3000 磅，它的预计 mpg 是多少？
可视化：用 plt.scatter() 画出测试集的真实数据点，并用 plt.plot() 画出你训练出的那条红色拟合直线
'''
#可视化特征
viz = cdf[['weight','mpg']]
viz.hist()
plt.show()

plt.scatter(cdf.weight, cdf.mpg, color='blue')
plt.xlabel("weight")
plt.ylabel("mpg")
plt.show()

#Pandas 的数据列（Series）转换为 NumPy 一维数组（ndarray）
x = cdf.weight.to_numpy()
y = cdf.mpg.to_numpy()


#分离数据，随机拆分为“训练集”和“测试集“
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


#训练模型
from sklearn import linear_model
regressor = linear_model.LinearRegression() #创造模型

regressor.fit(X_train.reshape(-1, 1), y_train) #-1 的意思是“让 Python 自己根据总元素个数自动算出行数”

print('斜率:', regressor.coef_[0])
print('截距:', regressor.intercept_)


#visualization of the regression line
plt.scatter(X_train, y_train, color='blue')
plt.plot(X_train, regressor.predict(X_train.reshape(-1, 1)), color='red', linewidth=2)
plt.xlabel("weight")
plt.ylabel("mpg")
plt.show()  


#model evaluation
from sklearn.metrics import mean_squared_error, r2_score
y_pred = regressor.predict(X_test.reshape(-1, 1))
print("均方误差: %.2f" % mean_squared_error(y_test, y_pred))
print('R2 score: %.2f' % r2_score(y_test, y_pred))


#预测新数据
input_weight = input("请输入新车的重量 (磅): ")
new_weight = float(input_weight)
predicted_mpg = regressor.predict(np.array([[new_weight]]))
print(f"预测一辆新车重量为 {new_weight} 磅时的燃油效率 (mpg): {predicted_mpg[0]:.2f}")

