#Principal Component Analysis (PCA)
import numpy as np
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#Standardize the data
iris = datasets.load_iris()
print("Original shape:", iris.data.shape)
print("missing values:", np.isnan(iris.data).sum())
X = iris.data
X_scaled = StandardScaler().fit_transform(X)

#Apply PCA to reduce the dimensionality of the data
pca = PCA(n_components=0.95)   
X_pca = pca.fit_transform(X_scaled)
print("自动选择的主成分个数:", pca.n_components_)

# Print the results
print("降维前形状:", X.shape)          # (150, 4)
print("降维后形状:", X_pca.shape)      # (150, 2)
print("每个主成分解释的方差比例:", pca.explained_variance_ratio_)
print("合计解释的方差:", pca.explained_variance_ratio_.sum())
print("主成分方向（每行一个主成分，每列对应一个原特征）:\n", pca.components_)
print("降维后的前 5 行:\n", X_pca[:5])



