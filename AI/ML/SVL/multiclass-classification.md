# 多分类逐行讲解：肥胖等级预测（One-vs-All 与 One-vs-One）

> **先说明**：我这边的网络拦住了 IBM 的数据链接，没能下载 `Obesity-level-prediction-dataset.csv`。我按这份数据的列名、列类型和行数（2111 行，17 列）造了一份**假数据**，把截图里的整段代码跑通了。所以文中的 **shape、类型、列名、报错**都是真的，但准确率等具体数字你自己跑会不一样。
>
> **最重要的一个坑**：新版 scikit-learn（我这里是 1.9.1）已经**删掉了** `LogisticRegression(multi_class='ovr')` 这个参数，直接跑会报 `TypeError: ... unexpected keyword argument 'multi_class'`。第 0 节给的代码已经改成能跑的写法，见第 8 节。

## 和上次「客户流失」逻辑回归比，变了什么

| | 上次：churn（二分类） | 这次：肥胖等级（多分类） |
|---|---|---|
| y 有几种值 | 2 种：0 / 1 | **7 种**：0~6，每个数代表一个肥胖等级 |
| y 原来长什么样 | 已经是数字 1.0/0.0，`astype('int')` 就行 | 是**文字**（`'Normal_Weight'`），要用 `.astype('category').cat.codes` 变成数字 |
| 输入 X | 全是数字 | 有数字列 **也有文字列**（性别、交通方式…），文字列要先**独热编码** |
| 模型 | 一个 `LogisticRegression` | 把多分类拆成很多个二分类：**OvA**（7 个模型）或 **OvO**（21 个模型） |
| 评价指标 | log loss | **accuracy**（预测对的比例） |
| `predict_proba` 每行 | 2 个数 `[P(0), P(1)]` | 7 个数，每个等级一个概率，加起来 = 1 |

一句话理论：逻辑回归本身只会回答"是/不是"。多分类就是**让它回答很多次"是/不是"，再汇总**。OvA 问"是不是 A 类？"×7 次；OvO 问"A 和 B 更像哪个？"×21 次然后投票。

---

## 0. 完整可运行代码（已修好 `multi_class` 报错）

```python
# ===== 导入 =====
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
warnings.filterwarnings('ignore')                       # 屏蔽警告，让输出干净

# ===== 1. 读数据 =====
file_path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/GkDzb7bWrtvGXdPOfk6CIg/Obesity-level-prediction-dataset.csv"
data = pd.read_csv(file_path)                           # 读 CSV → DataFrame，shape (2111, 17)
print(data.head())                                      # 看前 5 行

# ===== 2. EDA：看目标列每个等级有多少人 =====
sns.countplot(y='NObeyesdad', data=data)                # 横向柱状图，每个等级一根柱子
plt.title('Distribution of Obesity Levels')             # 给图加标题
plt.show()                                              # 显示图

data.info()                                             # 每列名字、非空个数、类型
print(data.describe())                                  # 数字列的均值、标准差、最小最大值等

# ===== 3. 标准化数字列 =====
continuous_columns = data.select_dtypes(include=['float64']).columns.tolist()  # 所有小数列的列名 → list
scaler = StandardScaler()                               # 建一个标准化工具（还没学任何东西）
scaled_features = scaler.fit_transform(data[continuous_columns])  # 学均值/标准差 + 变换，返回 ndarray (2111, 8)
scaled_df = pd.DataFrame(scaled_features, columns=scaler.get_feature_names_out(continuous_columns))  # 变回带列名的表
scaled_data = pd.concat([data.drop(columns=continuous_columns), scaled_df], axis=1)  # 去掉旧数字列，左右拼上新数字列

# ===== 4. 独热编码文字列 =====
categorical_columns = scaled_data.select_dtypes(include=['object']).columns.tolist()  # 所有文字列的列名
categorical_columns.remove('NObeyesdad')                # 目标列不编码，从 list 里删掉（直接改原 list）
encoder = OneHotEncoder(sparse_output=False, drop='first')  # 输出普通数组；每个特征丢掉第一个类别
encoded_features = encoder.fit_transform(scaled_data[categorical_columns])  # ndarray (2111, 15)
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_columns))
prepped_data = pd.concat([scaled_data.drop(columns=categorical_columns), encoded_df], axis=1)  # (2111, 24)

# ===== 5. 目标列：文字 → 数字 0~6 =====
prepped_data['NObeyesdad'] = prepped_data['NObeyesdad'].astype('category').cat.codes
print(prepped_data.head())

# ===== 6. 拆 X / y，再拆训练 / 测试 =====
X = prepped_data.drop('NObeyesdad', axis=1)             # 除目标列外的 23 列
y = prepped_data['NObeyesdad']                          # 目标列，Series (2111,)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ===== 7. One-vs-All（也叫 One-vs-Rest）=====
# 原代码：LogisticRegression(multi_class='ovr', max_iter=1000)  ← 新版 sklearn 会报错
model_ova = OneVsRestClassifier(LogisticRegression(max_iter=1000))   # ← 改了这一行
model_ova.fit(X_train, y_train)                         # 训练 7 个"是不是第 k 类"的二分类器
y_pred_ova = model_ova.predict(X_test)                  # 预测，ndarray (423,)，每个值 0~6
print("One-vs-All (OvA) Strategy")
print(f"Accuracy: {np.round(100*accuracy_score(y_test, y_pred_ova), 2)}%")

# ===== 8. One-vs-One =====
model_ovo = OneVsOneClassifier(LogisticRegression(max_iter=1000))    # 21 个"A 还是 B"的二分类器
model_ovo.fit(X_train, y_train)
y_pred_ovo = model_ovo.predict(X_test)
print("One-vs-One (OvO) Strategy")
print(f"Accuracy: {np.round(100*accuracy_score(y_test, y_pred_ovo), 2)}%")
```

**运行后会看到（假数据上的真实输出）**：

- `data.head()`：5 行 × 17 列的表格，最后一列 `NObeyesdad` 是文字，比如 `Normal_Weight`。
- 柱状图：纵轴是 7 个等级名字，横轴是人数，7 根横向柱子。课程说真实数据各等级人数差不多（"fairly balanced"）。
- `data.info()`：`dtypes: float64(8), object(9)`，即 8 个数字列、9 个文字列（新版 pandas 3 会把 `object` 显示成 `str`），所有列都是 2111 non-null，说明没有空值。
- 准确率两行，例如我这份假数据：`OvA 63.12%`、`OvO 90.07%`。你用真数据跑数字会不同。

---

## 1. 读数据和 EDA

### 点前面是谁

| 写法 | 点前面是谁 | 类型 | 从哪来 |
|---|---|---|---|
| `pd.read_csv(...)` | `pd` | 模块 | `import pandas as pd` |
| `data.head()` | `data` | DataFrame | `pd.read_csv` 返回的 |
| `sns.countplot(...)` | `sns` | 模块 | `import seaborn as sns` |
| `plt.title(...)`、`plt.show()` | `plt` | 模块 | `import matplotlib.pyplot as plt` |
| `data.info()`、`data.describe()` | `data` | DataFrame | 同上 |

### 点后面做了什么

| 写法 | 类型 | 作用 | 常用参数 | 返回什么 / 是否改原对象 |
|---|---|---|---|---|
| `pd.read_csv(file_path)` | 模块.函数 | 读 CSV 文件或网址 | `sep=','`、`nrows=100`（只读前 100 行） | **DataFrame** (2111, 17) |
| `data.head()` | 对象.方法() | 看前几行 | `n=5` | 新 DataFrame（5 行），不改 `data` |
| `sns.countplot(y='NObeyesdad', data=data)` | 模块.函数 | 数一数每个类别出现几次，画柱状图 | `y=` 横向柱、`x=` 竖向柱；`order=` 柱子顺序 | Axes 对象（画在当前图上） |
| `plt.title('...')` | 模块.函数 | 给**当前**图加标题 | `fontsize=14` | Text 对象 |
| `plt.show()` | 模块.函数 | 把图显示出来 | 无 | None |
| `data.info()` | 对象.方法() | **直接打印**列名、非空数、类型、内存 | 无 | **None**（所以 `print(data.info())` 会多打一行 `None`） |
| `data.describe()` | 对象.方法() | 数字列的统计摘要 | `include='all'` 连文字列也统计 | 新 DataFrame（8 行：count/mean/std/min/25%/50%/75%/max） |

**改参数试试**：`sns.countplot(x='NObeyesdad', data=data)` 把 `y` 改成 `x`，柱子变成竖的，但 7 个长名字会挤在一起，所以原代码用 `y`。

### 写法对照：`plt.title()` ↔ `ax.set_title()`

```python
# 你的代码用的是这种：plt 直接操作"当前图"
sns.countplot(y='NObeyesdad', data=data)
plt.title('Distribution of Obesity Levels')

# 等价写法：先拿到 Axes 对象 ax，再让 ax 自己设标题
ax = sns.countplot(y='NObeyesdad', data=data)   # countplot 返回 Axes
ax.set_title('Distribution of Obesity Levels')
```

### 举一反三：DataFrame 常用的其他点操作

| 写法 | 作用 |
|---|---|
| `data.shape` | 属性，(行数, 列数) → `(2111, 17)` |
| `data.columns` | 属性，所有列名 |
| `data.isnull().sum()` | 链式，每列空值个数（练习 1 要的"null 值"就是这个） |
| `data['NObeyesdad'].value_counts()` | 每个等级多少人，和柱状图同样的数字 |
| `data.dtypes` | 属性，每列的类型 |

---

## 2. 标准化数字列（StandardScaler）

一句话：把每个数字列变成"均值 0、标准差 1"，这样身高（1.7 左右）和体重（90 左右）在同一个尺度上，模型不会偏向数字大的列。

### 链式调用拆开：`data.select_dtypes(include=['float64']).columns.tolist()`

```python
step1 = data.select_dtypes(include=['float64'])  # DataFrame (2111, 8)：只留 8 个小数列
step2 = step1.columns                            # Index 对象：Index(['Age','Height','Weight','FCVC','NCP','CH2O','FAF','TUE'])
step3 = step2.tolist()                           # list：['Age', 'Height', ..., 'TUE']
continuous_columns = step3
```

| 写法 | 类型 | 作用 | 返回什么 |
|---|---|---|---|
| `.select_dtypes(include=['float64'])` | 对象.方法() | 按类型挑列 | 新 DataFrame，不改原 `data` |
| `.columns` | 对象.属性 | 取列名 | Index（pandas 自己的"列名清单"类型） |
| `.tolist()` | 对象.方法() | Index → 普通 Python list | **list**，所以后面才能用 `.remove()` |

### `scaler` 这几行

| 写法 | 类型 | 点前面是谁 | 作用 | 返回什么 / 是否改原对象 |
|---|---|---|---|---|
| `StandardScaler()` | 类（直接 import 的，不带点） | — | 建一个空的标准化工具 | StandardScaler 对象 |
| `scaler.fit_transform(data[continuous_columns])` | 对象.方法() | `scaler`，上一行建的 | **fit**：记下每列均值和标准差；**transform**：用它们变换数据 | **numpy ndarray** (2111, 8)，**列名丢了**；`data` 不变，但 `scaler` 自己身上记住了均值（`scaler.mean_`） |
| `scaler.get_feature_names_out(continuous_columns)` | 对象.方法() | `scaler` | 返回输出列的名字 | ndarray：`['Age' 'Height' ... 'TUE']`（标准化不改名，所以和输入一样） |
| `pd.DataFrame(scaled_features, columns=...)` | 模块.类 | `pd` | 把 ndarray 包回带列名的表 | DataFrame (2111, 8) |

### `pd.concat([...], axis=1)` 和 `data.drop(columns=...)`

```python
left  = data.drop(columns=continuous_columns)   # DataFrame (2111, 9)：去掉 8 个旧数字列，剩 9 个文字列
right = scaled_df                               # DataFrame (2111, 8)：标准化后的数字列
scaled_data = pd.concat([left, right], axis=1)  # DataFrame (2111, 17)：左右拼起来
```

| 写法 | 作用 | 关键参数 | 返回 / 是否改原对象 |
|---|---|---|---|
| `data.drop(columns=[...])` | 删掉这些列 | `columns=` 删列；`index=` 删行 | 新 DataFrame，**不改** `data`（除非 `inplace=True`） |
| `pd.concat([a, b], axis=1)` | 拼接多个表 | `axis=1` 左右拼（加列）；`axis=0` 上下拼（加行） | 新 DataFrame |

**改参数试试**：把 `axis=1` 改成 `axis=0`，会变成上下拼，结果 4222 行、17 列，而且一大堆 NaN（因为两个表的列名对不上）。

拼完之后列的**顺序变了**：文字列在前，数字列在后。不影响模型。

### 写法对照：`fit_transform` ↔ `fit` + `transform`

```python
scaled = scaler.fit_transform(X)            # 你的代码：一步到位
scaled = scaler.fit(X).transform(X)         # 上次 churn 代码的写法：fit 返回 scaler 自己，再接 transform
scaler.fit(X); scaled = scaler.transform(X) # 分两行，同样的结果
```

---

## 3. 独热编码文字列（OneHotEncoder）

一句话：模型只认数字。独热编码把一个文字列拆成几个 0/1 列，比如 `Gender` → `Gender_Male`（男 = 1，女 = 0）。

### `categorical_columns.remove('NObeyesdad')`

| 写法 | 类型 | 点前面是谁 | 作用 | 返回 / 是否改原对象 |
|---|---|---|---|---|
| `categorical_columns.remove('NObeyesdad')` | 对象.方法() | Python **list**（`.tolist()` 来的） | 从 list 里删掉第一个等于它的元素 | **返回 None，直接改原 list** |

坑：千万别写 `categorical_columns = categorical_columns.remove(...)`，那样变量会变成 `None`。我实测 `print(categorical_columns.remove('NObeyesdad'))` 打印的就是 `None`。

### `OneHotEncoder(sparse_output=False, drop='first')`

| 参数 | 作用 | 改了会怎样 |
|---|---|---|
| `sparse_output=False` | 输出普通 numpy 数组 | 改成 `True`（默认）→ 输出"稀疏矩阵"，省内存但不能直接塞进 `pd.DataFrame` |
| `drop='first'` | 每个特征丢掉第一个类别 | 去掉 → 列数从 15 变 **23**。丢一列不会丢信息：`Gender_Male=0` 就说明是女 |

实测 8 个文字列编码后变成 15 列：

```
['Gender_Male' 'family_history_with_overweight_yes' 'FAVC_yes'
 'CAEC_Frequently' 'CAEC_Sometimes' 'CAEC_no' 'SMOKE_yes' 'SCC_yes'
 'CALC_Frequently' 'CALC_Sometimes' 'CALC_no' 'MTRANS_Bike'
 'MTRANS_Motorbike' 'MTRANS_Public_Transportation' 'MTRANS_Walking']
```

可以看到：`CAEC` 有 4 个值（Always / Frequently / Sometimes / no），丢掉按字母排第一的 `Always`，剩 3 列。`get_feature_names_out` 在这里**有真正的作用**：它自动生成 `列名_类别` 形式的新名字。

| 写法 | 返回 |
|---|---|
| `encoder.fit_transform(scaled_data[categorical_columns])` | ndarray (2111, 15)，全是 0.0 / 1.0 |
| `encoder.get_feature_names_out(categorical_columns)` | 上面那 15 个新列名 |
| `encoder.categories_` | 属性，每个特征有哪些类别 |

最后 `pd.concat([scaled_data.drop(columns=categorical_columns), encoded_df], axis=1)` → **(2111, 24)**：8 个数字列 + 15 个独热列 + 1 个目标列，和课程说的"24 fields"一致。

### 写法对照：`OneHotEncoder` ↔ `pd.get_dummies`

```python
# 你的代码：sklearn 的 OneHotEncoder（能记住规则，之后能用同一规则处理新数据）
encoder = OneHotEncoder(sparse_output=False, drop='first')
encoded = encoder.fit_transform(df[cols])

# pandas 一行写法：直接返回 DataFrame，不用自己补列名，但不会"记住规则"
encoded_df = pd.get_dummies(df[cols], drop_first=True, dtype=float)
```

---

## 4. 目标列编码：`.astype('category').cat.codes`

```python
step1 = prepped_data['NObeyesdad']          # Series (2111,)，文字：'Normal_Weight' ...
step2 = step1.astype('category')            # Series，类型变成 category（"有固定几种值"的类型）
step3 = step2.cat                           # 属性：category 专用的工具箱（只有 category 类型才有 .cat）
step4 = step3.codes                         # 属性：每个值对应的编号，Series，类型 int8
prepped_data['NObeyesdad'] = step4          # 用数字覆盖原来的文字列
```

| 写法 | 类型 | 作用 | 返回 |
|---|---|---|---|
| `.astype('category')` | 对象.方法() | 换类型 | 新 Series，不改原列 |
| `.cat` | 对象.属性 | 进入 category 的专用工具 | 一个"访问器"对象 |
| `.codes` | 对象.属性（无括号） | 取编号 | Series，int8 |
| `.cat.categories` | 对象.属性 | 编号对应的原名字 | Index |

编号是按**字母顺序**给的，实测：

```
0: Insufficient_Weight   1: Normal_Weight      2: Obesity_Type_I
3: Obesity_Type_II       4: Obesity_Type_III   5: Overweight_Level_I
6: Overweight_Level_II
```

注意这只是名字的字母顺序，**不是**胖瘦顺序（5 号 Overweight 比 2 号 Obesity 还轻）。想查编号对应什么：`dict(enumerate(data['NObeyesdad'].astype('category').cat.categories))`。

### 写法对照

```python
y = df['NObeyesdad'].astype('category').cat.codes      # 你的代码
from sklearn.preprocessing import LabelEncoder
y = LabelEncoder().fit_transform(df['NObeyesdad'])     # sklearn 写法，同样按字母编号，返回 ndarray
codes, names = pd.factorize(df['NObeyesdad'])          # 按"出现顺序"编号，编号会不一样
```

---

## 5. 拆 X / y 和 `train_test_split`

```python
X = prepped_data.drop('NObeyesdad', axis=1)   # DataFrame (2111, 23)
y = prepped_data['NObeyesdad']                # Series (2111,)
```

`drop('NObeyesdad', axis=1)` 和前面的 `drop(columns='NObeyesdad')` 是**同一件事**的两种写法：`axis=1` 表示"按列删"。`axis=0` 是按行删，这里写成 0 会报 KeyError（找不到叫这个名字的行）。

`train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)`

| 参数 | 作用 | 改了会怎样 |
|---|---|---|
| `test_size=0.2` | 20% 当测试集 | 实测 X_train (1688, 23)，X_test (423, 23)；改成 0.3 → 测试集 634 行 |
| `random_state=42` | 固定随机种子 | 删掉 → 每次划分不同，准确率每次跑都会变一点 |
| `stratify=y` | **按 y 的比例分层抽样**，让训练集和测试集里 7 个等级的比例一样 | 这是二分类那次没用到的新参数，多分类时特别有用 |

`stratify=y` 的实测效果（7 个等级各占的比例）：

```
训练集: [0.075, 0.2, 0.156, 0.153, 0.248, 0.086, 0.082]
测试集: [0.073, 0.201, 0.156, 0.154, 0.248, 0.085, 0.083]
```

几乎一模一样。去掉 `stratify`，人数少的等级在测试集里可能偏多或偏少。

`train_test_split` 是"模块里的函数"，但写法上没有点，因为它是 `from sklearn.model_selection import train_test_split` 直接拿出来的。返回 **4 个东西**，按 `X_train, X_test, y_train, y_test` 的顺序接住。

---

## 6. 模型：One-vs-All 和 One-vs-One

### 两种策略一张表看懂

| | One-vs-All（OvA，也叫 One-vs-Rest / OvR） | One-vs-One（OvO） |
|---|---|---|
| 训练几个模型 | k 个 → **7 个** | k(k-1)/2 → **21 个** |
| 每个模型回答什么 | "是第 k 类，还是其他所有类？" | "是 A 类还是 B 类？"（只用这两类的数据训练） |
| 怎么出结果 | 7 个模型谁最有把握，就选谁 | 21 场"对决"投票，赢得最多的类胜出 |
| 实测 `len(model.estimators_)` | 7 | 21 |

`model.estimators_` 是属性，里面装着训练好的那一堆小模型，可以用 `len()` 数一数。

### 点操作

| 写法 | 类型 | 点前面是谁 | 作用 | 返回 / 是否改原对象 |
|---|---|---|---|---|
| `LogisticRegression(max_iter=1000)` | 类 | — | 建一个逻辑回归模型 | 模型对象 |
| `OneVsOneClassifier(LogisticRegression(...))` | 类，把另一个模型**包在里面** | — | "用这个模型做模板，造 21 个" | OvO 模型对象 |
| `model_ova.fit(X_train, y_train)` | 对象.方法() | 模型对象 | 训练 | **返回模型自己，并直接修改模型**（学到的参数存在模型身上） |
| `model_ova.predict(X_test)` | 对象.方法() | 训练好的模型 | 给每行预测一个类别 | ndarray (423,)，值是 0~6，实测前 10 个：`[4 2 2 2 1 4 1 1 2 2]` |
| `model_ova.predict_proba(X_test)` | 对象.方法() | 同上 | 每行 7 个概率 | ndarray (423, 7)。OvO 的 `OneVsOneClassifier` **没有**这个方法 |

`max_iter=1000`：最多迭代 1000 次。改小成 `max_iter=50`，会出现 `ConvergenceWarning`（没训练完），准确率可能下降。数据多、类别多时默认的 100 次常常不够。

### 评价：`accuracy_score` 和 `np.round`

```python
acc = accuracy_score(y_test, y_pred_ova)   # 函数（直接 import 的）：预测对的比例，float，比如 0.6312
pct = 100 * acc                            # 63.12...
shown = np.round(pct, 2)                   # 模块.函数：保留 2 位小数 → 63.12
print(f"Accuracy: {shown}%")               # f-string：{} 里的东西会被算出来塞进字符串
```

| 写法 | 对照写法 |
|---|---|
| `np.round(x, 2)`（你的代码） | `round(x, 2)`（Python 自带）；`f"{x:.2f}"`（在 f-string 里直接格式化） |
| `accuracy_score(y_test, y_pred)` | `model.score(X_test, y_test)`：模型自己算准确率，结果一样 |

---

## 7. `multi_class='ovr'` 报错（重要）

**最可能的原因**：你用的 scikit-learn 版本太新，`multi_class` 参数已经被删掉了（1.5 版开始提示要删，我实测 1.9.1 已经没有）。

报错长这样：

```
TypeError: LogisticRegression.__init__() got an unexpected keyword argument 'multi_class'
```

修改（只改了 `model_ova = ...` 这一行）：

```python
from sklearn.multiclass import OneVsRestClassifier            # ← 新增 import

# model_ova = LogisticRegression(multi_class='ovr', max_iter=1000)    # 旧写法，新版报错
model_ova = OneVsRestClassifier(LogisticRegression(max_iter=1000))   # ← 改了这一行
model_ova.fit(X_train, y_train)
```

写法对照，三种"多分类逻辑回归"：

| 写法 | 做法 | 你的代码 |
|---|---|---|
| `LogisticRegression(multi_class='ovr')` | OvA，旧版本写法 | 原代码用的这个（新版报错） |
| `OneVsRestClassifier(LogisticRegression())` | OvA，新写法，效果同上 | 修好后用这个 |
| `LogisticRegression()` 什么都不加 | 直接做多分类（叫 multinomial / softmax），**不是** OvA | 注释里写"(default)"，但默认其实不是 OvA |
| `OneVsOneClassifier(LogisticRegression())` | OvO | 第二个模型用这个 |

想知道自己装的是哪个版本：`import sklearn; print(sklearn.__version__)`。

---

## 常见坑

1. **`multi_class` 报错**：见上一节，换成 `OneVsRestClassifier`。
2. **`list.remove()` 返回 None**：只写 `categorical_columns.remove('NObeyesdad')`，不要把结果赋值回去。
3. **`print(data.info())` 多打一个 `None`**：`info()` 自己就会打印，返回 None。直接写 `data.info()` 就行。

## 动手试试

1. 把 `drop='first'` 删掉，再 `print(prepped_data.shape)`，看列数从 24 变成多少（应该是 32），再看准确率有没有变化。
2. 把 `stratify=y` 删掉，打印 `y_test.value_counts(normalize=True).sort_index()`，和上面的比例对比。

## 自己查点操作

- `type(scaled_features)` → 看到 `numpy.ndarray`，就知道为什么后面要 `pd.DataFrame(...)` 包回去。
- `dir(model_ova)` → 能看到 `fit`、`predict`、`predict_proba`、`estimators_` 等。
- `help(OneHotEncoder)` 或 Jupyter 里光标放在 `OneHotEncoder(` 后按 Shift+Tab，看所有参数。
