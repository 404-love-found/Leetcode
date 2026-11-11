import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
import pandas as pd

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
df = pd.read_csv(url)
df.head()
X = df.drop(columns="species").values          # 4 个特征，(150, 4)
y = df["species"].astype("category").cat.codes # 品种 → 0/1/2，只用来上色

#standardize the data
X_scaled = StandardScaler().fit_transform(X)

#decomposition and manifold learning models
models = {
    "PCA":   PCA(n_components=2),
    "t-SNE": TSNE(n_components=2, perplexity=30, random_state=42),
    "UMAP":  umap.UMAP(n_components=2, min_dist=0.5, random_state=42),
}

#plot the results
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, (name, model) in zip(axes, models.items()):
    Z = model.fit_transform(X_scaled)
    ax.scatter(Z[:, 0], Z[:, 1], c=y, cmap="viridis", s=30, alpha=0.7, edgecolor="k")
    ax.set_title(name)
    ax.set_xticks([]); ax.set_yticks([])
plt.show()
