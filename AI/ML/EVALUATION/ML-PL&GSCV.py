#Machine Learning Pipelines and GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
import seaborn as sns

#Load the Iris dataset and split into training and testing sets
data = load_iris()
print(data.DESCR)
#split the dataset into features and target variable
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

#Create a machine learning pipeline with StandardScaler, PCA, and KNeighborsClassifier
base_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=2)),
    ('knn', KNeighborsClassifier(n_neighbors=5))
])

#train the pipeline on the training data
base_pipeline.fit(X_train, y_train)
base_score = base_pipeline.score(X_test, y_test)
y_base_pred = base_pipeline.predict(X_test)
print(f"Base Pipeline Accuracy: {base_score:.4f}")
print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_base_pred)}")

#Define a parameter grid for GridSearchCV to tune hyperparameters of the pipeline

tuning_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA()),
    ('knn', KNeighborsClassifier())
])

param_grid = {
    'pca__n_components': [2, 3],
    'knn__n_neighbors': [3, 5, 7]
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

#Perform GridSearchCV to find the best hyperparameters for the pipeline
best_model = GridSearchCV(
    estimator=tuning_pipeline,
    param_grid=param_grid,
    scoring='accuracy',
    cv=cv,
    verbose=1
)

best_model.fit(X_train, y_train)
best_score = best_model.best_score_
best_params = best_model.best_params_
print(f"Best Cross-Validation Accuracy: {best_score:.4f}")
print(f"Best Hyperparameters: {best_params}")
print(f"Test Set Accuracy: {best_model.score(X_test, y_test):.4f}")
print(f"Confusion Matrix:\n{confusion_matrix(y_test, best_model.predict(X_test))}")