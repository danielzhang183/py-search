import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

# 加载客户数据
data = pd.read_csv('customer_data.csv')
features = data[['purchase_history', 'browsing_behavior', 'age', 'gender']]
X = features.values

K = 4
kmeans = KMeans(n_clusters=K, random_state=0)
kmeans.fit(X)

# 获取聚类标签
labels = kmeans.labels_
data['cluster'] = labels

for i in range(K):
    cluster_data = data[data['cluster'] == i]
    print(f"Cluster {i+1} Characteristics:")
    print(f"Number of Customers: {len(cluster_data)}")
    print(f"Average Age: {cluster_data['age'].mean()}")
    print(f"Gender Distribution: {cluster_data['gender'].value_counts()}")
print("\n")
