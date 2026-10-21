# 决策树（drug200）KeyError: 'Drug_num' 修复

## 一句话原因

你建列的时候起名叫 `'Drug map'`（中间是空格），后面取列的时候写的却是 `'Drug_num'`。DataFrame 里根本没有叫 `Drug_num` 的列，所以报 `KeyError`。

改掉列名以后，还有一个**不报错、但结果是错的**问题：drug200 的 `Drug` 列实际的取值是 `drugY, drugX, drugA, drugB, drugC`，你的 `custom_map` 里写的是 `drugA ~ drugE`，**没有 drugX 和 drugY**（多出来的 drugD、drugE 数据里也没有）。`.map()` 找不到的值会变成 `NaN`，200 行里有大约 145 行（drugY 约 91 行 + drugX 约 54 行）会是 NaN，相关系数就只是拿剩下那几十行算出来的。

> 说明：我这边的网络打不开那个数据链接，所以没能替你跑一遍。上面的取值和数量来自这个公开数据集的已知内容。你可以自己用下面代码里的 `print(my_data['Drug'].unique())` 那行确认一下。

---

## 修改后的完整代码

改动处都用 `# ★ 改` 标出来了。

```python
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import metrics
# ★ 改：删掉了 import matplotlib_inline（这里没用到，它是给 Jupyter 用的；没装的话还会报 ModuleNotFoundError）

import warnings
warnings.filterwarnings('ignore')   # 关掉警告信息

# ===== 1. 读数据 =====
path = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/drug200.csv'
my_data = pd.read_csv(path)          # 读成一个 DataFrame，shape (200, 6)

print("data info:")
my_data.info()                       # ★ 改：info() 自己会打印，并且返回 None；原来写在 print 里会多打出一个 "None"
print("missing values:\n", my_data.isnull().sum())   # 每列有几个缺失值，这个数据全是 0

# ★ 新增：先看清 Drug 列到底有哪些值，再写映射表
print("Drug 的取值:", my_data['Drug'].unique())
# 会看到类似：['drugY' 'drugC' 'drugX' 'drugA' 'drugB']

# ===== 2. 把文字特征变成数字 =====
label_encoder = LabelEncoder()
my_data['Sex'] = label_encoder.fit_transform(my_data['Sex'])                  # F→0, M→1
my_data['BP'] = label_encoder.fit_transform(my_data['BP'])                    # HIGH→0, LOW→1, NORMAL→2
my_data['Cholesterol'] = label_encoder.fit_transform(my_data['Cholesterol'])  # HIGH→0, NORMAL→1
print(my_data.head())                # ★ 改：只看前 5 行，原来 print(my_data) 会刷出 200 行

# ===== 3. 给 Drug 建一个数字版本，用来算相关系数 =====
custom_map = {'drugA': 0, 'drugB': 1, 'drugC': 2, 'drugX': 3, 'drugY': 4}   # ★ 改：键换成数据里真实存在的 5 个值
my_data['Drug_num'] = my_data['Drug'].map(custom_map)                         # ★ 改：列名从 'Drug map' 改成 'Drug_num'，和后面一致
print("映射失败(NaN)的行数:", my_data['Drug_num'].isnull().sum())             # ★ 新增：应该是 0；不是 0 说明映射表漏了值

# ===== 4. 相关系数 =====
corr = my_data.drop('Drug', axis=1).corr()['Drug_num']   # 去掉文字列 Drug，算所有数字列两两相关，再取 Drug_num 那一列
print(corr)

# ===== 5. 画每种药的数量 =====
category_counts = my_data['Drug'].value_counts()          # 每种药出现几次，从多到少排
plt.bar(category_counts.index, category_counts.values, color='blue')
plt.xlabel('Drug')
plt.ylabel('Count')
plt.title('Category Distribution')
plt.xticks(rotation=45)
plt.show()

# ===== 6. 建模 =====
y = my_data['Drug']                                       # 标签用原始文字就行，决策树能直接处理
X = my_data.drop(['Drug', 'Drug_num'], axis=1)            # 特征：Age, Sex, BP, Cholesterol, Na_to_K，shape (200, 5)
X_trainset, X_testset, y_trainset, y_testset = train_test_split(
    X, y, test_size=0.3, random_state=42)                 # 140 行训练，60 行测试
drugTree = DecisionTreeClassifier(criterion="entropy", max_depth=4)
drugTree.fit(X_trainset, y_trainset)

# ===== 7. 评估 =====
tree_predictions = drugTree.predict(X_testset)
print("Decision Trees's Accuracy: ", metrics.accuracy_score(y_testset, tree_predictions))

# ===== 8. 画树 =====
plt.figure(figsize=(14, 8))                                # ★ 新增：把图放大，不然字挤在一起
plot_tree(drugTree,
          feature_names=X.columns,                         # ★ 新增：节点上显示 "Na_to_K <= 14.6" 而不是 "x[4] <= 14.6"
          class_names=drugTree.classes_,                   # ★ 新增：叶子上显示药名
          filled=True)                                     # ★ 新增：按类别上色
plt.show()
```

### 运行后会看到什么

- `info()`：200 行、6 列，`Age` 和 `Na_to_K` 是数字，其余 4 列是 `object`（文字）。
- 缺失值：每列都是 0。
- `Drug 的取值`：5 个药名。
- `映射失败(NaN)的行数: 0`。
- `corr`：一列数字，`Drug_num` 自己是 1.0。`Na_to_K` 的相关性最明显（这个数据集里 Na_to_K 大的人基本都用 drugY）。
- 柱状图：drugY 最高（约 91），然后 drugX（约 54），drugA（约 23），drugB、drugC 各约 16。
- 准确率：通常在 0.98 左右，sklearn 版本不同可能略有差别。
- 树图：根节点基本都是按 `Na_to_K` 来切分。

---

## 点操作拆解

### 1. 先认点前面是谁

| 名字 | 是什么 | 从哪来 |
|---|---|---|
| `pd` | pandas 模块的别名 | `import pandas as pd` |
| `plt` | matplotlib 的 pyplot 模块 | `from matplotlib import pyplot as plt` |
| `metrics` | sklearn 里放评估函数的模块 | `from sklearn import metrics` |
| `warnings` | Python 自带模块 | `import warnings` |
| `my_data` | **DataFrame**（表格） | `pd.read_csv(path)` 返回的 |
| `my_data['Drug']` | **Series**（表格里的一列） | 用 `[列名]` 从 DataFrame 取出来的 |
| `label_encoder` | **LabelEncoder 对象** | `LabelEncoder()` 创建的 |
| `category_counts` | **Series**（索引是药名，值是次数） | `value_counts()` 返回的 |
| `drugTree` | **DecisionTreeClassifier 模型对象** | `DecisionTreeClassifier(...)` 创建的 |

### 2. 每个点操作做了什么

| 写法 | 类型 | 作用 | 改原对象吗 | 返回什么 |
|---|---|---|---|---|
| `warnings.filterwarnings('ignore')` | 模块.函数 | 不再显示警告 | 改全局设置 | `None` |
| `pd.read_csv(path)` | 模块.函数 | 读 csv（本地路径或网址都行） | — | DataFrame |
| `my_data.info()` | 对象.方法 | 打印列名、类型、非空数量 | 不改 | **`None`**（所以别放进 print） |
| `my_data['Drug'].unique()` | 对象.方法 | 列出这一列不重复的值 | 不改 | ndarray |
| `label_encoder.fit_transform(列)` | 对象.方法 | 先记住有哪些类别（fit），再把文字换成 0,1,2…（transform） | 不改传进去的列，但会**改 label_encoder 自己**（记住新的类别） | ndarray |
| `my_data.head()` | 对象.方法 | 取前 5 行，`head(10)` 就是前 10 行 | 不改 | DataFrame |
| `my_data['Drug'].map(custom_map)` | 对象.方法 | 按字典把每个值替换掉，**字典里找不到的变 NaN** | 不改 | Series |
| `my_data['Drug_num'].isnull().sum()` | 链式 | 数一下有几个 NaN | 不改 | 一个整数 |
| `my_data.drop('Drug', axis=1)` | 对象.方法 | 删掉 Drug 列，`axis=1` 表示删列，`axis=0` 表示删行 | **默认不改**原表 | 新 DataFrame |
| `.corr()` | 对象.方法 | 所有数字列两两算相关系数 | 不改 | DataFrame（方阵，6×6） |
| `my_data['Drug'].value_counts()` | 对象.方法 | 数每个值出现几次，从多到少 | 不改 | Series |
| `category_counts.index` | 对象.属性 | 这个 Series 的"标签"，这里是药名 | — | Index |
| `category_counts.values` | 对象.属性 | 这个 Series 的数字，这里是次数 | — | ndarray |
| `plt.bar(x, h, color=)` | 模块.函数 | 画柱状图 | 画到当前图上 | 一组柱子对象 |
| `plt.xlabel / ylabel / title` | 模块.函数 | 设置 x 轴名、y 轴名、标题 | 改当前图 | 文字对象 |
| `plt.xticks(rotation=45)` | 模块.函数 | x 轴刻度文字倾斜 45° | 改当前图 | 刻度信息 |
| `plt.figure(figsize=(14, 8))` | 模块.函数 | 新建一张图，宽 14、高 8 英寸 | 新建 | Figure |
| `plt.show()` | 模块.函数 | 弹出窗口显示图 | — | `None` |
| `drugTree.fit(X, y)` | 对象.方法 | 用训练数据训练这棵树 | **直接改 drugTree 本身** | drugTree 自己 |
| `drugTree.predict(X_testset)` | 对象.方法 | 对新数据给出预测的药名 | 不改 | ndarray，长度 60 |
| `drugTree.classes_` | 对象.属性 | 模型学到的类别名，`fit` 之后才有（结尾带 `_` 的属性都是训练后才有） | — | ndarray |
| `X.columns` | 对象.属性 | DataFrame 的列名 | — | Index |
| `metrics.accuracy_score(真, 预测)` | 模块.函数 | 预测对的比例 | — | 一个小数 |

`train_test_split`、`DecisionTreeClassifier`、`plot_tree` 是用 `from ... import` 直接拿进来的，所以前面没有点。等价写法是 `sklearn.model_selection.train_test_split(...)`。

### 3. 链式调用逐步拆开

**`my_data.drop('Drug', axis=1).corr()['Drug_num']`**（报错就出在这一行）

```python
step1 = my_data.drop('Drug', axis=1)   # DataFrame，shape (200, 6)：Age, Sex, BP, Cholesterol, Na_to_K, Drug_num
step2 = step1.corr()                   # DataFrame，shape (6, 6)：行和列都是上面 6 个列名
step3 = step2['Drug_num']              # Series，长度 6：其他每一列和 Drug_num 的相关系数
```

原来报错是在 `step3` 这一步：`step2` 的列名里有 `'Drug map'`，没有 `'Drug_num'`。以后遇到 KeyError，先 `print(某个DataFrame.columns)` 看一眼真实的列名。

**`my_data.isnull().sum()`**

```python
step1 = my_data.isnull()   # DataFrame，shape (200, 6)，每格是 True/False（是不是缺失）
step2 = step1.sum()        # Series，长度 6：每列 True 的个数（True 算 1，False 算 0）
```

### 4. 同一功能的不同写法

| 功能 | 写法 A | 写法 B | 你的代码用的 |
|---|---|---|---|
| 设置标题 | `plt.title('...')` | `fig, ax = plt.subplots()` 后用 `ax.set_title('...')` | A |
| 文字变数字 | `LabelEncoder().fit_transform(列)` | `列.map({'F':0, 'M':1})` | 特征用 A，Drug 用 B |
| 删列 | `df.drop('Drug', axis=1)` | `df.drop(columns='Drug')` | A（B 更不容易写错 axis） |
| 求和 | `np.sum(arr)` | `arr.sum()` | 用的是 B 形式：`.isnull().sum()` |

### 5. 举一反三：DataFrame 和模型对象上其他常用的点操作

- `my_data.shape`：属性，(行数, 列数)
- `my_data.describe()`：每个数字列的均值、最大最小值等
- `my_data['BP'].nunique()`：这一列有几种不同的值
- `drugTree.feature_importances_`：每个特征有多重要（加起来是 1）
- `drugTree.get_depth()`：树实际长了几层

---

## 常见坑

1. **`map` 不会报错，只会悄悄产生 NaN。** 写完映射一定要 `.isnull().sum()` 检查一下，这次的 drugX/drugY 就是这样漏掉的。
2. **`info()` 返回 `None`。** 它和 `print`、`plt.show()`、`list.append()` 一样是"直接做事、不返回结果"的类型，不要放进 `print(...)`，也不要赋值给变量。
3. **给没有顺序的类别编号后算相关系数，意义不大。** drugA=0、drugY=4 只是随便排的号，换一种排法相关系数就变了。想看哪个特征有用，`drugTree.feature_importances_` 更靠谱。项目里讲[多分类](multiclass-classification.md)的那篇也是直接把文字标签交给模型，和这里 `y = my_data['Drug']` 是一样的做法。

## 动手试试

1. 把 `max_depth=4` 改成 `max_depth=1` 再跑：准确率会明显下降，树图只剩一次切分（基本就是 `Na_to_K`）。改成 `max_depth=None` 看看树会长多深（`drugTree.get_depth()`）。
2. 在训练完之后加一行 `print(dict(zip(X.columns, drugTree.feature_importances_)))`，看看哪个特征最重要。

## 自己查的办法

- `type(my_data.info())` → 会看到 `NoneType`，就知道它不返回东西。
- `print(my_data.columns)` → 碰到 KeyError 第一件事就是看真实列名。
- `help(pd.Series.map)` 或在 Jupyter 里按 Shift+Tab → 看 `map` 的用法和参数。
