import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

# 1. 造数据：4 个中心，标准差不同 → 团的"密度"不同
centers = [[2, -6, -6], [-1, 9, 4], [-8, 7, 2], [4, 7, 9]]
X, y = make_blobs(n_samples=500, centers=centers,
                  cluster_std=[1, 1, 2, 3.5], random_state=42)

# 2. 标准化（Exercise 2 的答案）
X_scaled = StandardScaler().fit_transform(X)

# 3. 三种降维方法，接口相同：fit_transform → (500, 2)
models = {
    "PCA":   PCA(n_components=2),
    "t-SNE": TSNE(n_components=2, perplexity=30, random_state=42),
    "UMAP":  umap.UMAP(n_components=2, min_dist=0.5, random_state=42),
}

# 4. 并排画图对比
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, (name, model) in zip(axes, models.items()):
    Z = model.fit_transform(X_scaled)
    ax.scatter(Z[:, 0], Z[:, 1], c=y, cmap="viridis", s=30, alpha=0.7, edgecolor="k")
    ax.set_title(name)
    ax.set_xticks([]); ax.set_yticks([])
plt.show()