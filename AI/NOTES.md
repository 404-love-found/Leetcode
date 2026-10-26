
# Part 1. Organized notes

## 1.1 Load and look at the data

```python
import pandas as pd

data = pd.read_csv(url)     # module.function: read a CSV file into a DataFrame (a table)
data.info()                 # object.method: prints column names, non-null counts, dtypes; returns None, so don't wrap it in print()
data.head()                 # first 5 rows, returns a DataFrame
data['Class']               # one column → Series
data[['a', 'b']]            # several columns (double brackets) → DataFrame
data.iloc[:, 1:30]          # by position: all rows, columns 1..29 (end excluded) → DataFrame
```

## 1.2 Check missing values and class balance

```python
data.isnull().sum()         # chained: True/False table → missing count per column (Series)
data.isnull().sum().sum()   # one more .sum() → total missing cells in the whole table (int)
data['Class'].value_counts()  # Series method: how many times each value appears, largest first
```

## 1.3 Correlation with the target

```python
corr = data.corr(numeric_only=True)['Y'].drop('Y')   # 'Y' = the column you want to predict
#      └ DataFrame (all vs all) └ Series: each column vs Y └ remove Y vs itself (always 1.0)
corr = corr.sort_values(ascending=False)  # ascending=False → large to small; must assign back
corr.abs()                  # absolute value of each entry, returns a NEW Series (strength regardless of sign)
corr.index                  # the labels of this Series = the feature names
corr.values                 # just the numbers, as an ndarray

ax = corr.plot(kind='barh', figsize=(10, 6))   # returns an Axes
# kind: 'line' (default), 'bar' vertical bars, 'barh' horizontal bars, 'hist' histogram
# figsize=(width, height) in inches
```

## 1.4 Turn a table into arrays

| Code | What it does | Returns |
|---|---|---|
| `df.values` | drops column names and row labels, keeps only numbers (attribute, no brackets) | ndarray, shape `(rows, columns)` |
| `df.to_numpy()` | same thing, the form pandas now recommends (method) | ndarray |
| `np.asarray(df)` | same thing, numpy's function | ndarray |

## 1.5 Scaling

```python
from sklearn.preprocessing import StandardScaler, normalize

scaler = StandardScaler()          # create an empty tool
X_std = scaler.fit_transform(X)    # learn each column's mean & std, return (X - mean) / std as a new ndarray
X_new_std = scaler.transform(X_new)  # new data: reuse what was learned, never fit again

X_l1 = normalize(X, norm='l1')     # function, no fitting: rescales each ROW
```

| | `StandardScaler` | `normalize` |
|---|---|---|
| Works on | each **column** | each **row** |
| After | each column has mean 0, std 1 | each row's absolute values sum to 1 (`'l1'`), or each row has length 1 (`'l2'`, default) |
| Needs `fit`? | yes, remembers mean/std | no, each row is handled on its own |
| Used in | linear, logistic, multiclass, fraud | regression tree, fraud |

## 1.6 Split

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# test_size=0.3 → 30% for testing; random_state fixes the shuffle so results repeat
# add stratify=y for classification so train and test keep the same class proportions
```

## 1.7 Build a model

```python
DecisionTreeRegressor(criterion='squared_error', max_depth=d, random_state=42)
# criterion: how a split is judged ('squared_error' → leaf = mean, 'absolute_error' → leaf = median)
# max_depth: most questions from root to leaf; bigger → fits training data more closely, can overfit
dt.fit(X_train, y_train, sample_weight=w_train)
# sample_weight: how much each row counts; compute_sample_weight('balanced', y_train) makes rare classes count more
```

## 1.8 Plot

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()     # Figure (whole canvas) + Axes (one plotting area)
ax.set_title('...')          # title of that plotting area   (same as plt.title('...'))
ax.set_xlabel('...')         # x-axis label                  (same as plt.xlabel('...'))
plt.tight_layout()           # fix margins so labels aren't cut off — before show()
plt.show()                   # actually display the chart; in a .py script nothing appears without it
```

---

# Part 2. Steps 4–6 for every model

What changes from model to model is mostly **which predict method** you call and **which metric** you use:

| Method | Gives | Available on |
|---|---|---|
| `model.predict(X)` | final answer: a number or a class | every model |
| `model.predict_proba(X)` | probability of each class, rows sum to 1 | classifiers except `LinearSVC` |
| `model.decision_function(X)` | raw score (distance from the boundary) | `LogisticRegression`, `LinearSVC`, `OneVsOneClassifier` |
| `model.score(X, y)` | R² (regressors) or accuracy (classifiers) | every model |

## Model 1. Multiple linear regression (mpg)

```python
# ===== 4. Build + train =====
model = LinearRegression()                  # create an empty model
model.fit(X_train, y_train)                 # learn coef_ and intercept_; modifies model itself
print(model.coef_, model.intercept_)        # attributes that exist only after fit

# ===== 5. Predict =====
y_pred = model.predict(X_test)              # ndarray (79, 1): predicted mpg per car
# no predict_proba / decision_function: regression gives numbers, not classes

# ===== 6. Test =====
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print("MSE :", mean_squared_error(y_test, y_pred))    # average squared error, smaller is better
print("MAE :", mean_absolute_error(y_test, y_pred))   # average error in mpg, smaller is better
print("R²  :", r2_score(y_test, y_pred))              # closer to 1 is better
print("train R²:", model.score(X_train, y_train))     # compare with test R² to spot overfitting
```

Real output on `mpg.csv`: MSE 10.6, MAE 2.51, test R² 0.792, train R² 0.81. Train and test are close, so no overfitting.

## Model 2. Logistic regression (churn, 0/1)

```python
# ===== 4. Build + train =====
LR = LogisticRegression()                   # C=1.0 by default: smaller C → coefficients pushed toward 0
LR.fit(X_train, y_train)

# ===== 5. Predict =====
yhat = LR.predict(X_test)                   # ndarray (40,): 0 or 1
yhat_prob = LR.predict_proba(X_test)        # ndarray (40, 2): [P(0), P(1)] per row
z = LR.decision_function(X_test)            # ndarray (40,): raw score; > 0 ⇔ P(1) > 0.5 ⇔ predict 1

# ===== 6. Test =====
from sklearn.metrics import log_loss, accuracy_score, confusion_matrix, roc_auc_score
print("log loss:", log_loss(y_test, yhat_prob))              # uses probabilities; guessing = 0.693
print("accuracy:", accuracy_score(y_test, yhat))             # same as LR.score(X_test, y_test)
print("ROC-AUC :", roc_auc_score(y_test, yhat_prob[:, 1]))   # uses the P(1) column
print(confusion_matrix(y_test, yhat))                        # rows = actual, columns = predicted
```

## Model 3. Multiclass: One-vs-Rest and One-vs-One (7 obesity levels)

```python
# ===== 4. Build + train =====
model_ova = OneVsRestClassifier(LogisticRegression(max_iter=1000))  # wraps 7 binary models
model_ovo = OneVsOneClassifier(LogisticRegression(max_iter=1000))   # wraps 21 binary models (7×6/2)
model_ova.fit(X_train, y_train)
model_ovo.fit(X_train, y_train)
print(len(model_ova.estimators_), len(model_ovo.estimators_))      # 7 21

# ===== 5. Predict =====
y_pred_ova = model_ova.predict(X_test)        # ndarray (423,): class code 0..6
y_pred_ovo = model_ovo.predict(X_test)
proba_ova = model_ova.predict_proba(X_test)   # ndarray (423, 7): one probability per level
score_ovo = model_ovo.decision_function(X_test)  # ndarray (423, 7): vote-based scores; OvO has no predict_proba

# ===== 6. Test =====
from sklearn.metrics import accuracy_score, classification_report
print("OvA accuracy:", accuracy_score(y_test, y_pred_ova))
print("OvO accuracy:", accuracy_score(y_test, y_pred_ovo))
print(classification_report(y_test, y_pred_ova, target_names=list(class_names)))  # per-level precision/recall
```

## Model 4. Decision tree classifier (drug200)

```python
# ===== 4. Build + train =====
drugTree = DecisionTreeClassifier(criterion="entropy", max_depth=4)
drugTree.fit(X_train, y_train)
print(drugTree.get_depth(), drugTree.get_n_leaves())   # actual depth and number of leaves

# ===== 5. Predict =====
y_pred = drugTree.predict(X_test)             # ndarray (60,): drug names
proba = drugTree.predict_proba(X_test)        # ndarray (60, 5): share of each drug in that row's leaf
print(drugTree.classes_)                      # column order of proba: ['drugA' 'drugB' 'drugC' 'drugX' 'drugY']

# ===== 6. Test =====
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
print("accuracy:", accuracy_score(y_test, y_pred))                   # ≈ 0.98 on the real data
print(confusion_matrix(y_test, y_pred, labels=drugTree.classes_))   # 5×5
print(classification_report(y_test, y_pred, zero_division=0))       # per-drug precision/recall
```

## Model 5. Regression tree (taxi tip)

```python
# ===== 4. Build + train =====
dt_reg = DecisionTreeRegressor(criterion='squared_error', max_depth=8, random_state=35)
dt_reg.fit(X_train, y_train)

# ===== 5. Predict =====
y_pred = dt_reg.predict(X_test)               # 1-D ndarray: each value = average tip in that leaf
# no predict_proba: a regressor has no classes

# ===== 6. Test =====
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
mse = mean_squared_error(y_test, y_pred)
print("MSE :", mse)                                    # course reference: in the twenties
print("RMSE:", np.sqrt(mse))                           # back in dollars
print("MAE :", mean_absolute_error(y_test, y_pred))    # average miss in dollars
print("R²  :", r2_score(y_test, y_pred))               # same as dt_reg.score(X_test, y_test); reference ≈ 0.03
```

## Model 6. Credit card fraud: decision tree + LinearSVC

```python
# ===== 4. Build + train =====
w_train = compute_sample_weight('balanced', y_train)   # fraud rows weigh ~580× more (284315 / 492)
dt = DecisionTreeClassifier(max_depth=4, random_state=35)
dt.fit(X_train, y_train, sample_weight=w_train)

svm = LinearSVC(class_weight='balanced', random_state=42, loss='hinge', fit_intercept=False)
svm.fit(X_train, y_train)                              # class_weight does the same job as sample_weight

# ===== 5. Predict =====
dt_label  = dt.predict(X_test)                         # 0/1
dt_score  = dt.predict_proba(X_test)[:, 1]             # P(fraud)
svm_label = svm.predict(X_test)                        # 0/1
svm_score = svm.decision_function(X_test)              # distance from boundary; LinearSVC has no predict_proba

# ===== 6. Test =====
from sklearn.metrics import roc_auc_score, recall_score, precision_score, confusion_matrix
print("DT  ROC-AUC:", roc_auc_score(y_test, dt_score))     # needs a score, not 0/1 labels
print("SVM ROC-AUC:", roc_auc_score(y_test, svm_score))
print("DT  recall :", recall_score(y_test, dt_label))      # share of real fraud caught
print("DT  precision:", precision_score(y_test, dt_label)) # share of "fraud" alarms that were real
print(confusion_matrix(y_test, svm_label))                 # bottom row: [missed fraud, caught fraud]
# don't use accuracy here: always saying "not fraud" already scores 99.83%
```

---