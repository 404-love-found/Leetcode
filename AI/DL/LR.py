'''
线性回归训练,机器学习Linear Regression Training, Machine Learning
'''
from matplotlib.path import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib_inline

#载入数据
# 1. 自动获取 LR.py 所在目录 (AI/DL/) 下的 mpg.csv 路径
csv_path = Path(__file__).parent / 'mpg.csv'
data = pd.read_csv(csv_path)

#检测数据
data.sample(5)
