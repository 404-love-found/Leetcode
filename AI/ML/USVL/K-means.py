import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans 
from sklearn.datasets import make_blobs 
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import seaborn as sns
import matplotlib_inline

import warnings
warnings.filterwarnings('ignore')


cust_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%204/data/Cust_Segmentation.csv")
cust_df.info()
print("missing values:",cust_df.isnull().sum().sum())
cust_df = cust_df.drop('Address', axis=1)            # delete the column has words
cust_df = cust_df.dropna()                           # delte the line has null





#Elbow method to choose the best K
inertias = []
for k in range(1, 9):                                    
    km = KMeans(n_clusters=k, n_init=12, random_state=0).fit(X)
    inertias.append(km.inertia_)                        
plt.plot(range(1, 9), inertias, 'o-')                    
plt.xlabel('n_clusters'); plt.ylabel('inertia')
plt.show()


#train the model
k_means = KMeans(init = "k-means++", 
                 n_clusters = 4, 
                 n_init = 12)
k_means.fit(X)

k_means_labels = k_means.labels_                   #cluster id of each point
k_means_cluster_centers = k_means.cluster_centers_ #center coordinates
k_means_cluster_distance = k_means.inertia_        #sum of squared distances from points to their center




