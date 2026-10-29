'''
Comparing Random Forest and XGBoost modeling performance
'''
import time                                          # 计时
import numpy as np                                   # 数值计算
import pandas as pd                                  # 表格（DataFrame）
import matplotlib.pyplot as plt                      # 画图
from sklearn.model_selection import train_test_split # 切分训练集 / 测试集
from sklearn.ensemble import RandomForestRegressor   # 随机森林（回归）
from xgboost import XGBRegressor                     # XGBoost（回归）
from sklearn.metrics import mean_squared_error, r2_score   # 评估指标

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/UZPRFNucrENAFm25csq6eQ/California-housing.csv")
df.info()
print("Missing_values:",df.isnull().sum().sum())


#correlation
Correlation_values = df.corr(numeric_only=True)['Target'].drop('Target')
Correlation_values = Correlation_values.abs().sort_values(ascending=True)
print("Correlation:",Correlation_values)

# Separate features and target
X = df.drop(columns=["Target"])
y = df["Target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Observe 
N_observations, N_features = X.shape
print('Number of Observations: ' + str(N_observations))
print('Number of Features: ' + str(N_features))

#Build the model
n_estimators = 100
RF = RandomForestRegressor(n_estimators=n_estimators,random_state=42)
XG = XGBRegressor(n_estimators=n_estimators,random_state=42)

#train and count the train time for eah model

#=====Random Forest====
start = time.perf_counter()
RF.fit(X_train,y_train)
RF_pred_y = RF.predict(X_test)
RF_train_time = time.perf_counter() -start
#=====XGboost=====
start = time.perf_counter()
XG.fit(X_train,y_train)
XG_pred_y = XG.predict(X_test)
XG_train_time = time.perf_counter() -start


#Predict
# ===== 6. 评估（只算一次、只打印一次） =====
mse_rf = mean_squared_error(y_test, RF_pred_y)
mse_xgb = mean_squared_error(y_test, XG_pred_y)
r2_rf = r2_score(y_test, RF_pred_y)
r2_xgb = r2_score(y_test, XG_pred_y)
std_y = np.std(y_test)                               # 真实房价的波动幅度，当作"尺子"

print(f"Random Forest:  MSE = {mse_rf:.4f}, R^2 = {r2_rf:.4f}")
print(f"      XGBoost:  MSE = {mse_xgb:.4f}, R^2 = {r2_xgb:.4f}")
print(f"Random Forest:  Training Time = {RF_train_time:.3f}s")
print(f"      XGBoost:  Training Time = {XG_train_time:.3f}s")
print(f"Std of y_test = {std_y:.4f}")
print(f"RF  RMSE = {np.sqrt(mse_rf):.4f}  (比 std_y 小 = 比永远猜平均值强)")
print(f"XGB RMSE = {np.sqrt(mse_xgb):.4f}")

