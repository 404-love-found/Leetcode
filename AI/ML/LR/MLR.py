'''
多重线性回归/Multiple Linear Regression

Predict MPG with Multiple Linear Regression
X = Weight、Horsepower、Model Year
y = MPG
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("AI/ML/mpg.csv")

# verify successful load with some randomly selected records
df.sample(5)

df.describe()

# Drop categoricals and any useless columns
df = df.drop(['origin', 'name'], axis=1)

# Drop rows with missing values (horsepower has 6 missing)
df = df.dropna()

df.corr()

# Keep only weight, horsepower, model_year and mpg
df = df.drop(['cylinders', 'displacement', 'acceleration'], axis=1)

df.head(9)

axes = pd.plotting.scatter_matrix(df, alpha=0.2)
# need to rotate axis labels so we can read them
for ax in axes.flatten():
    ax.xaxis.label.set_rotation(90)
    ax.yaxis.label.set_rotation(0)
    ax.yaxis.label.set_ha('right')
plt.tight_layout()
plt.gcf().subplots_adjust(wspace=0, hspace=0)
plt.show()

# Extract the input features (X) and the target (y)
X = df[['weight', 'horsepower', 'model_year']].to_numpy()
y = df[['mpg']].to_numpy()

from sklearn import preprocessing

std_scaler = preprocessing.StandardScaler()
X_std = std_scaler.fit_transform(X)

pd.DataFrame(X_std).describe().round(2)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, random_state=42)

from sklearn import linear_model

# create a model object
regressor = linear_model.LinearRegression()

# train the model in the training data
regressor.fit(X_train, y_train)

# Print the coefficients
coef_ = regressor.coef_
intercept_ = regressor.intercept_

print('Coefficients: ', coef_)
print('Intercept: ', intercept_)

# Get the standard scaler's mean and standard deviation parameters
means_ = std_scaler.mean_
std_devs_ = np.sqrt(std_scaler.var_)

# The least squares parameters relative to the original, unstandardized feature space:
coef_original = coef_ / std_devs_
intercept_original = intercept_ - np.sum((means_ * coef_) / std_devs_)

print('Coefficients: ', coef_original)
print('Intercept: ', intercept_original)

# ---- 3D plot: weight (column 0) and model_year (column 2) ----
# horsepower is held at its mean (0 after standardizing)
X1 = X_test[:, 0]
X2 = X_test[:, 2]

# Create a mesh grid for plotting the regression plane
x1_surf, x2_surf = np.meshgrid(np.linspace(X1.min(), X1.max(), 100),
                               np.linspace(X2.min(), X2.max(), 100))

y_surf = intercept_ + coef_[0, 0] * x1_surf + coef_[0, 2] * x2_surf

# Predict y values to compare with actual y_test for above/below plane colors
y_pred = regressor.predict(X_test)
above_plane = y_test >= y_pred
below_plane = y_test < y_pred
above_plane = above_plane[:, 0]
below_plane = below_plane[:, 0]

# Plotting
fig = plt.figure(figsize=(20, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the data points above and below the plane in different colors
ax.scatter(X1[above_plane], X2[above_plane], y_test[above_plane, 0], label="Above Plane", s=70, alpha=.7, ec='k')
ax.scatter(X1[below_plane], X2[below_plane], y_test[below_plane, 0], label="Below Plane", s=50, alpha=.3, ec='k')

# Plot the regression plane
ax.plot_surface(x1_surf, x2_surf, y_surf, color='k', alpha=0.21, label='plane')

# Set view and labels
ax.view_init(elev=10)
ax.legend(fontsize='x-large', loc='upper center')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_box_aspect(None, zoom=0.75)
ax.set_xlabel('WEIGHT', fontsize='xx-large')
ax.set_ylabel('MODEL YEAR', fontsize='xx-large')
ax.set_zlabel('MPG', fontsize='xx-large')
ax.set_title('Multiple Linear Regression of MPG', fontsize='xx-large')
plt.tight_layout()
plt.show()

# ---- One 2D plot per feature ----
plt.scatter(X_train[:, 0], y_train, color='blue')
plt.plot(X_train[:, 0], coef_[0, 0] * X_train[:, 0] + intercept_[0], '-r')
plt.xlabel("Weight")
plt.ylabel("MPG")
plt.show()

plt.scatter(X_train[:, 1], y_train, color='blue')
plt.plot(X_train[:, 1], coef_[0, 1] * X_train[:, 1] + intercept_[0], '-r')
plt.xlabel("Horsepower")
plt.ylabel("MPG")
plt.show()

plt.scatter(X_train[:, 2], y_train, color='blue')
plt.plot(X_train[:, 2], coef_[0, 2] * X_train[:, 2] + intercept_[0], '-r')
plt.xlabel("Model Year")
plt.ylabel("MPG")
plt.show()