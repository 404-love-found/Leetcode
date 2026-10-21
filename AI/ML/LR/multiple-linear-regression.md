# 多重线性回归逐行讲解：从 `from sklearn import preprocessing` 开始

> 我用你上传的 `mpg.csv` 把整段代码真实跑了一遍（去掉缺失值后 392 行），下面所有数字都是实际输出。你自己跑时结果应该一模一样，因为 `random_state=42` 固定了随机划分。

在进入 sklearn 之前，先记住两个东西长什么样：

- `X`：形状 `(392, 3)` 的 NumPy 数组，三列依次是 **weight、horsepower、model_year**。
- `y`：形状 `(392, 1)` 的 NumPy 数组，只有一列 **mpg**。注意 `df[['mpg']]` 用了两层方括号，所以是二维的“列向量”，不是一维数组。这一点后面会影响 `coef_` 和 `intercept_` 的形状。

我们要找的模型是：

```
mpg = b + w1·weight + w2·horsepower + w3·model_year
```

`b` 叫截距 (intercept)，`w1, w2, w3` 叫系数 (coefficients)。“训练”就是找出让预测值和真实值误差平方和最小的那组 `b, w1, w2, w3`，这个方法叫**最小二乘法**。

---

## 第 1 段：标准化 (Standardization)

```python
from sklearn import preprocessing

std_scaler = preprocessing.StandardScaler()
X_std = std_scaler.fit_transform(X)

pd.DataFrame(X_std).describe().round(2)
```

### 每行在做什么

| 代码 | 含义 |
|---|---|
| `from sklearn import preprocessing` | 从 scikit-learn 导入“数据预处理”模块，里面有各种缩放、编码工具。 |
| `preprocessing.StandardScaler()` | 创建一个“标准化器”对象。此时它什么都还没学，只是一个空工具。 |
| `std_scaler.fit_transform(X)` | 一步做两件事：**fit** 计算每一列的均值和标准差并记在对象里；**transform** 用这些数把每个值变成 `(x - 均值) / 标准差`。 |
| `pd.DataFrame(X_std).describe().round(2)` | 把结果转成表格看统计量，保留两位小数，用来检查标准化是否成功。 |

### 为什么要标准化

原始三列的尺度差别非常大：

| | weight | horsepower | model_year |
|---|---|---|---|
| 均值 | 2977.58 | 104.47 | 75.98 |
| 标准差 | 849.40 | 38.49 | 3.68 |

weight 动辄几千，model_year 只在 70 到 82 之间。标准化之后，每一列都变成**均值 0、标准差 1**，单位统一成“偏离平均水平多少个标准差”。好处有两个：

1. **系数可以直接比较大小**。标准化后，系数大小就代表“这个特征变化 1 个标准差，mpg 变多少”，三个特征站在同一起跑线上。
2. 对梯度下降类、带正则化的模型（Ridge、Lasso、神经网络）很重要。普通的 `LinearRegression` 本身不需要标准化也能算出等价的结果（后面第 5 段会证明），但养成习惯有好处。

### 实际输出

```
            0       1       2
count  392.00  392.00  392.00
mean    -0.00   -0.00   -0.00
std      1.00    1.00    1.00
min     -1.61   -1.52   -1.63
max      2.55    3.27    1.64
```

均值是 0（`-0.00` 只是浮点误差），标准差是 1，说明成功了。

举个例子，第一辆车（chevrolet chevelle malibu）原始值 `[3504, 130, 70]`，标准化后是 `[0.621, 0.664, -1.625]`。意思是：它比平均车重 0.62 个标准差、马力高 0.66 个标准差、年份早 1.6 个标准差。

> 小细节：`StandardScaler` 算的标准差是 848.32，而 `describe()` 显示 849.40。差别来自分母：sklearn 除以 n，pandas 除以 n-1。不影响理解。

---

## 第 2 段：划分训练集和测试集

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, random_state=42)
```

### 每个参数的意思

| 参数 | 含义 |
|---|---|
| `X_std, y` | 要切分的特征和目标，两者的行会一一对应地被切开，不会错位。 |
| `test_size=0.2` | 20% 的行做测试集，80% 做训练集。 |
| `random_state=42` | 随机种子。切分前会打乱顺序，固定种子后每次打乱方式都一样，结果可复现。42 只是惯例，换别的数也行。 |

返回 4 个数组，顺序固定是 **X_train, X_test, y_train, y_test**，顺序写错是新手常见 bug。

实际形状：

```
X_train (313, 3)   X_test (79, 3)
y_train (313, 1)   y_test (79, 1)
```

### 为什么要分开

模型只能在训练集上“学习”。测试集相当于期末考试的新题，用来检查模型面对**没见过的数据**表现如何。如果用同一批数据训练又测试，就像用练习册原题考试，分数会虚高，看不出是否“死记硬背”（过拟合）。

> 进阶提醒：你的代码是**先对全部数据标准化，再切分**，严格来说测试集的信息（它的均值、标准差）已经“泄露”进了标准化。更规范的写法是先切分，再 `scaler.fit(X_train)`，然后分别 `transform` 训练集和测试集。在这个数据集上影响很小，但在正式项目里要注意。

---

## 第 3 段：创建并训练线性回归模型

```python
from sklearn import linear_model

# create a model object
regressor = linear_model.LinearRegression()

# train the model in the training data
regressor.fit(X_train, y_train)
```

| 代码 | 含义 |
|---|---|
| `from sklearn import linear_model` | 导入线性模型模块（里面还有 Ridge、Lasso、LogisticRegression 等）。 |
| `linear_model.LinearRegression()` | 创建一个普通最小二乘线性回归模型对象，此时参数还是空的。 |
| `regressor.fit(X_train, y_train)` | **训练**。sklearn 用最小二乘法直接算出让训练集误差平方和最小的截距和系数，存进 `regressor` 里。 |

sklearn 几乎所有模型都遵循同一个套路，学会一个就会全部：

```
model = 某模型()        # 1. 创建
model.fit(X, y)        # 2. 训练
model.predict(X_new)   # 3. 预测
model.score(X, y)      # 4. 评分（回归默认是 R²）
```

顺便看看模型好不好（这两行不在你的代码里，是我加的检查）：

```
训练集 R² = 0.810
测试集 R² = 0.792
```

R² 越接近 1 越好，0.79 表示模型解释了测试集中大约 79% 的 mpg 变化。训练和测试的分数接近，说明没有明显过拟合。

---

## 第 4 段：查看系数和截距

```python
coef_ = regressor.coef_
intercept_ = regressor.intercept_

print('Coefficients: ', coef_)
print('Intercept: ', intercept_)
```

sklearn 里**以下划线结尾的属性**（`coef_`、`intercept_`、`mean_`）都表示“训练之后才有的、学出来的东西”。

实际输出：

```
Coefficients:  [[-5.49994399 -0.3386371   2.79376226]]
Intercept:  [23.4826366]
```

- `coef_` 形状是 `(1, 3)`：1 个目标 × 3 个特征。之所以是二维，是因为 `y` 是二维的 `(n, 1)`。所以后面要写 `coef_[0, 0]` 才能取到第一个数。
- `intercept_` 形状是 `(1,)`，所以后面写 `intercept_[0]`。

### 怎么解读（标准化空间里）

| 特征 | 系数 | 含义 |
|---|---|---|
| weight | **-5.50** | 车重每增加 1 个标准差（约 848 磅），mpg 下降约 5.5 |
| horsepower | -0.34 | 马力每增加 1 个标准差，mpg 只下降 0.34 |
| model_year | **+2.79** | 年份每晚 1 个标准差（约 3.7 年），mpg 上升约 2.8 |

截距 23.48：当三个标准化特征都等于 0，也就是**三项都是平均水平**的车，模型预测 mpg 约 23.5。

因为是标准化后的系数，可以直接比较：**weight 影响最大，其次 model_year，horsepower 很小**。horsepower 小不代表马力和油耗无关，而是马力和车重高度相关，“马力的信息”大多已经被 weight 带走了（这叫多重共线性）。

---

## 第 5 段：把系数换回原始单位

标准化后的系数不好直接用，比如你想知道“车重每多 1 磅，mpg 变多少”。这一段就是把系数翻译回原始单位。

```python
means_ = std_scaler.mean_
std_devs_ = np.sqrt(std_scaler.var_)

coef_original = coef_ / std_devs_
intercept_original = intercept_ - np.sum((means_ * coef_) / std_devs_)
```

| 代码 | 含义 |
|---|---|
| `std_scaler.mean_` | 标准化器在 fit 时记住的每列均值：`[2977.58, 104.47, 75.98]` |
| `std_scaler.var_` | 每列方差；开根号 `np.sqrt` 得到标准差：`[848.32, 38.44, 3.68]` |
| `coef_ / std_devs_` | 每个系数除以对应列的标准差（NumPy 会按列逐个相除，这叫广播） |
| `np.sum(...)` | 把三项加起来，用来修正截距 |

### 公式从哪来（推导很短）

标准化后的模型是：

```
mpg = b + w · z,  其中 z = (x - μ) / σ
```

把 `z` 代进去展开：

```
mpg = b + w · (x - μ) / σ
    = b + (w/σ)·x  -  (w·μ/σ)
    = [b - Σ(w·μ/σ)]  +  (w/σ)·x
       ↑ 新截距              ↑ 新系数
```

所以：

- **原始系数 = w / σ**，对应 `coef_ / std_devs_`
- **原始截距 = b − Σ(w·μ/σ)**，对应 `intercept_ - np.sum((means_ * coef_) / std_devs_)`

### 实际输出

```
Coefficients:  [[-0.00648335 -0.00880903  0.75937368]]
Intercept:  [-13.98927584]
```

写成方程就是：

```
mpg ≈ -13.99 - 0.00648·weight - 0.00881·horsepower + 0.759·model_year
```

现在可以用日常语言解释了：

- 车重每多 **1 磅**，mpg 降 0.0065，也就是每多 **1000 磅**降约 6.5。
- 马力每多 **1 hp**，mpg 降约 0.0088。
- 年份每晚 **1 年**，mpg 升约 0.76（70 年代末的车更省油）。
- 截距 -13.99 本身没有物理意义（重量 0、马力 0、1900 年的车不存在），它只是让平面落在正确位置。

> 我额外验证了一下：直接用**未标准化**的数据训练 `LinearRegression`，得到的系数和截距与上面完全一样。这说明对普通线性回归来说，标准化不改变模型本身，只改变系数的“单位”。

> 注意：原始系数**不能**用来比较哪个特征更重要，因为单位不同（磅 vs 马力 vs 年）。比较重要性要看第 4 段的标准化系数。

---

## 第 6 段：3D 回归平面图

三个特征加上 mpg 一共 4 维，画不出来。所以这里只挑 **weight（第 0 列）和 model_year（第 2 列）** 做 x、y 轴，mpg 做 z 轴，horsepower 固定在 0，也就是固定在平均水平。

### 6.1 取出要画的两列

```python
X1 = X_test[:, 0]   # 所有行的第 0 列 → weight（标准化后）
X2 = X_test[:, 2]   # 所有行的第 2 列 → model_year（标准化后）
```

`[:, 0]` 是 NumPy 切片：冒号表示“所有行”，0 表示“第 0 列”。

### 6.2 生成网格，用来画平面

```python
x1_surf, x2_surf = np.meshgrid(np.linspace(X1.min(), X1.max(), 100),
                               np.linspace(X2.min(), X2.max(), 100))
```

- `np.linspace(a, b, 100)`：在 a 到 b 之间均匀取 100 个点。
- `np.meshgrid(...)`：把两组 100 个点组合成 100×100 的网格，得到两个 `(100, 100)` 矩阵，每个格点都有一对 (weight, year) 坐标。画曲面必须要这种网格。

### 6.3 算出平面上每个点的 mpg

```python
y_surf = intercept_ + coef_[0, 0] * x1_surf + coef_[0, 2] * x2_surf
```

就是模型方程 `b + w1·weight + w3·year`。horsepower 那一项 `w2 · 0 = 0`，所以被省掉了，这就是“马力固定在平均值”的意思。

### 6.4 判断每个测试点在平面上方还是下方

```python
y_pred = regressor.predict(X_test)      # 模型对 79 个测试样本的预测，形状 (79, 1)
above_plane = y_test >= y_pred          # 真实值 ≥ 预测值 → True，形状 (79, 1)
below_plane = y_test < y_pred
above_plane = above_plane[:, 0]         # 压成一维 (79,)，才能当索引用
below_plane = below_plane[:, 0]
```

`above_plane` 是一个由 True/False 组成的“布尔掩码”。`X1[above_plane]` 的意思是“只取出 True 位置的那些值”。实际结果是 39 个点在上方、40 个点在下方，基本对半，说明模型没有系统性地高估或低估。

前 5 个测试样本的预测和真实值对比：

```
预测：25.89  26.11  33.04  26.63  29.43
真实：26.0   21.6   36.1   26.0   27.0
```

> 小细节：`y_pred` 是用**完整三个特征**算的，而画出来的平面把 horsepower 固定为 0。所以某个点被标成“上方”，是相对真实模型而言，不一定严格对应图里那张平面。看图时不必太较真。

### 6.5 画图

```python
fig = plt.figure(figsize=(20, 8))              # 新建画布，宽 20 高 8 英寸
ax = fig.add_subplot(111, projection='3d')     # 加一个 3D 坐标系；111 = 1行1列第1个
```

```python
ax.scatter(X1[above_plane], X2[above_plane], y_test[above_plane, 0],
           label="Above Plane", s=70, alpha=.7, ec='k')
ax.scatter(X1[below_plane], X2[below_plane], y_test[below_plane, 0],
           label="Below Plane", s=50, alpha=.3, ec='k')
```

画两组散点，参数含义：`s` 点的大小，`alpha` 透明度（0 全透明，1 不透明），`ec='k'` 点的边框颜色为黑色（k = black），`label` 用于图例。上方的点画得更大更实，下方的点更小更淡，这样能看出平面“穿过”点云。

```python
ax.plot_surface(x1_surf, x2_surf, y_surf, color='k', alpha=0.21, label='plane')
```

用前面的网格画出半透明的黑色回归平面。

```python
ax.view_init(elev=10)                 # 视角：仰角 10 度，几乎平视
ax.legend(fontsize='x-large', loc='upper center')   # 图例放上方中间
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])   # 去掉刻度数字（标准化后的数字没什么直观意义）
ax.set_box_aspect(None, zoom=0.75)    # 整体缩小一点，防止标签被裁掉
ax.set_xlabel('WEIGHT', ...)          # 三个轴的名字
ax.set_ylabel('MODEL YEAR', ...)
ax.set_zlabel('MPG', ...)
ax.set_title('Multiple Linear Regression of MPG', ...)
plt.tight_layout()                    # 自动调整边距
plt.show()                            # 显示图像
```

运行结果（我保留了刻度数字方便你对照，你的代码会把它们隐藏）：

![3D 回归平面](img/3d_plane.png)

从图上可以看出：越往“重”的方向，平面越低（mpg 越低）；越往“新”的年份，平面越高。

---

## 第 7 段：每个特征一张 2D 图

```python
plt.scatter(X_train[:, 0], y_train, color='blue')
plt.plot(X_train[:, 0], coef_[0, 0] * X_train[:, 0] + intercept_[0], '-r')
plt.xlabel("Weight")
plt.ylabel("MPG")
plt.show()
```

后面两段完全一样，只是把列号换成 1（Horsepower）和 2（Model Year）。

| 代码 | 含义 |
|---|---|
| `plt.scatter(X_train[:, 0], y_train, color='blue')` | 蓝色散点：横轴是训练集的 weight（标准化），纵轴是真实 mpg。 |
| `coef_[0, 0] * X_train[:, 0] + intercept_[0]` | 只用 weight 这一项算出的预测值：`b + w1·weight`，相当于假设另外两个特征都在平均水平。 |
| `plt.plot(..., '-r')` | 用红色实线 (`-` 实线，`r` 红色) 把这些预测值连起来，是一条直线。 |

运行结果（我把三张拼在一起了）：

![三个特征的 2D 图](img/2d_lines.png)

### 怎么看这三张图

- **Weight**：红线向下倾斜明显，斜率 -5.5，和点的趋势吻合。
- **Horsepower**：红线几乎是平的（斜率只有 -0.34），但蓝点明显是向下的！这不是 bug。原因是这条线表示“**在车重和年份不变的前提下**”马力的单独影响，而马力的大部分影响已经算到 weight 头上了。这正是多重回归和单变量回归的区别。
- **Model Year**：红线向上，越新的车越省油。

另外注意，红线不一定穿过点云的正中间，因为每张图只展示了模型的一个“切面”，其他两个特征的贡献被固定在平均值了。

---

## 总结：整条流程

```
原始 X (392×3)
   │  StandardScaler.fit_transform    → 每列变成均值0、标准差1
   ▼
X_std
   │  train_test_split(0.2, 42)       → 313 训练 / 79 测试
   ▼
X_train, y_train
   │  LinearRegression().fit          → 最小二乘求 b 和 w
   ▼
coef_ = [-5.50, -0.34, 2.79], intercept_ = 23.48   （标准化单位，可比较重要性）
   │  w/σ,  b − Σ(wμ/σ)
   ▼
原始单位方程：mpg ≈ -13.99 − 0.00648·weight − 0.00881·hp + 0.759·year
   │
   ▼
3D 平面图（weight × year）+ 三张 2D 切面图
```

如果你想继续深入，可以试试这几个练习：

1. 用 `regressor.score(X_test, y_test)` 自己算 R²，再用 `from sklearn.metrics import mean_squared_error` 算误差。
2. 改成“先切分、再只在训练集上 fit scaler”的写法，看结果变化多少。
3. 去掉 horsepower 只用两个特征训练，看 R² 下降多少。
4. 用原始单位方程手算一辆车的 mpg，比如 3000 磅、100 马力、1980 年款，和 `regressor.predict` 的结果对比（记得先用 `std_scaler.transform` 标准化输入）。
