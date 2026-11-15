import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def make_models(lasso_alpha):
    return {'Ordinary': LinearRegression(),
            'Ridge': Ridge(alpha=1.0),
            'Lasso': Lasso(alpha=lasso_alpha)}


def report(y_true, y_pred, name):
    mse = mean_squared_error(y_true, y_pred)
    print(f'{name:9s} R2={r2_score(y_true, y_pred):.4f}  '
          f'MAE={mean_absolute_error(y_true, y_pred):.4f}  RMSE={np.sqrt(mse):.4f}')


# ---------- Part 1: 单特征，有 / 无离群点 ----------
np.random.seed(42)
X = 2 * np.random.rand(1000, 1)
y = 4 + 3 * X.ravel() + np.random.randn(1000)

y_outlier = y.copy()
idx = np.random.choice(np.where(X.ravel() > 1.5)[0], 5, replace=False)
y_outlier[idx] += np.random.uniform(50, 100, 5)

for title, y_fit in [('Trained with outliers', y_outlier), ('Trained without outliers', y)]:
    print(title)
    for name, model in make_models(lasso_alpha=0.2).items():
        report(y, model.fit(X, y_fit).predict(X), name)   # 始终用干净的 y 评分
    print()


# ---------- Part 2: 100 个特征，只有 10 个有用 ----------
X2, y2, ideal_coef = make_regression(n_samples=100, n_features=100, n_informative=10,
                                     noise=10, random_state=42, coef=True)


def compare(X_data, title):
    X_tr, X_te, y_tr, y_te = train_test_split(X_data, y2, test_size=0.3, random_state=42)
    print(title)
    fitted = {}
    for name, model in make_models(lasso_alpha=0.1).items():
        report(y_te, model.fit(X_tr, y_tr).predict(X_te), name)
        fitted[name] = model
    print()
    return fitted


fitted = compare(X2, 'All 100 features')

# 特征选择：保留 Lasso 系数绝对值 > 5 的特征
selected = np.where(np.abs(fitted['Lasso'].coef_) > 5)[0]
print('Selected:         ', selected)
print('Truly informative:', np.where(ideal_coef != 0)[0], '\n')

compare(X2[:, selected], f'{len(selected)} Lasso-selected features')