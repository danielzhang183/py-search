# K-means聚类分析指南

参考文章：[K-means聚类算法：原理、实例与代码分析](https://developer.aliyun.com/article/1541894)

## 简介

K-means是一种常用的无监督学习算法，用于将数据分成K个不同的聚类。本项目提供了完整的K-means聚类分析功能，可以方便地对CSV数据进行聚类分析。

## 安装依赖

```bash
pip install pandas scikit-learn numpy
```

或者：

```bash
pip install -r requirements.txt
```

## 基本使用

### 方式1: 使用便捷函数

```python
from py_search.data_analyzer import kmeans_analyze_csv

# 对CSV文件进行聚类分析
result = kmeans_analyze_csv(
    csv_file="example.csv",
    n_clusters=3,  # 分为3个聚类
    directory="./data"
)

# 查看结果
print(f"聚类数: {result['n_clusters']}")
print(f"总样本数: {result['total_samples']}")
print(f"使用的列: {result['used_columns']}")

# 查看各聚类的统计信息
for cluster_id, info in result['cluster_info'].items():
    print(f"\n聚类 {cluster_id}:")
    print(f"  样本数: {info['count']}")
    print(f"  平均值: {info['mean']}")
```

### 方式2: 使用类方法

```python
from py_search import CSVReader
from py_search.data_analyzer import DataAnalyzer

# 读取CSV文件
reader = CSVReader(directory="./data")
df = reader.read_with_pandas("example.csv")

# 创建分析器
analyzer = DataAnalyzer()

# 数据预处理
data, columns = analyzer.preprocess_data(df)

# 执行聚类
result = analyzer.kmeans_cluster(data, n_clusters=3)

# 查看结果
print(f"聚类标签: {result['labels']}")
print(f"聚类中心: {result['centers']}")
print(f"轮廓系数: {result['silhouette_score']}")
```

## 寻找最优聚类数

使用肘部法则和轮廓系数找到最优的聚类数：

```python
from py_search import CSVReader
from py_search.data_analyzer import DataAnalyzer

reader = CSVReader(directory="./data")
df = reader.read_with_pandas("example.csv")

analyzer = DataAnalyzer()
data, _ = analyzer.preprocess_data(df)

# 寻找最优聚类数（测试2-10个聚类）
optimal = analyzer.find_optimal_clusters(data, max_clusters=10)

print(f"最优聚类数: {optimal['optimal_k']}")
print(f"\n各聚类数的轮廓系数:")
for k, score in zip(optimal['k_range'], optimal['silhouette_scores']):
    marker = " ← 最优" if k == optimal['optimal_k'] else ""
    print(f"  k={k}: {score:.4f}{marker}")
```

## 客户细分示例

参考阿里云文章中的客户细分场景：

```python
from py_search.data_analyzer import kmeans_analyze_csv

# 假设CSV文件包含以下列：
# - 客户ID
# - 消费金额
# - 购买次数
# - 最近购买天数

result = kmeans_analyze_csv(
    csv_file="customer_data.csv",
    n_clusters=4,  # 将客户分为4类
    numeric_columns=["消费金额", "购买次数", "最近购买天数"],
    directory="./data"
)

# 查看每个客户所属的聚类
df = result['dataframe']
print(df[['客户ID', 'cluster']].head(20))

# 分析每个客户群体的特征
for cluster_id, info in result['cluster_info'].items():
    print(f"\n客户群体 {cluster_id}:")
    print(f"  客户数量: {info['count']}")
    print(f"  平均消费金额: {info['mean'].get('消费金额', 0):.2f}")
    print(f"  平均购买次数: {info['mean'].get('购买次数', 0):.2f}")
```

## 参数说明

### kmeans_analyze_csv 函数

- `csv_file`: CSV文件名或路径
- `n_clusters`: 聚类数量，默认为3
- `numeric_columns`: 要使用的数值列列表，如果为None则自动选择所有数值列
- `directory`: CSV文件所在目录

### DataAnalyzer.kmeans_cluster 方法

- `data`: 输入数据（numpy数组）
- `n_clusters`: 聚类数量
- `random_state`: 随机种子，默认为42
- `max_iter`: 最大迭代次数，默认为300

### DataAnalyzer.find_optimal_clusters 方法

- `data`: 输入数据
- `max_clusters`: 最大聚类数，默认为10
- `random_state`: 随机种子

## 结果说明

### 聚类结果字典

```python
{
    'labels': array([0, 1, 2, ...]),  # 每个样本的聚类标签
    'centers': array([[...], ...]),   # 聚类中心坐标
    'cluster_counts': {0: 10, 1: 15, 2: 8},  # 每个聚类的样本数
    'n_clusters': 3,                   # 聚类数量
    'silhouette_score': 0.65,         # 轮廓系数（-1到1，越大越好）
    'inertia': 123.45                  # 簇内平方和（越小越好）
}
```

### 分析结果字典

```python
{
    'file': 'example.csv',             # 文件名
    'n_clusters': 3,                   # 聚类数
    'used_columns': ['列1', '列2'],    # 使用的列
    'cluster_result': {...},           # 聚类结果
    'cluster_info': {                  # 各聚类统计信息
        0: {'count': 10, 'mean': {...}},
        1: {'count': 15, 'mean': {...}},
        ...
    },
    'dataframe': DataFrame,            # 包含聚类标签的DataFrame
    'total_samples': 33                # 总样本数
}
```

## 评估指标

### 轮廓系数 (Silhouette Score)

- 范围：-1 到 1
- 值越大越好
- 接近1：样本被很好地分配到聚类中
- 接近0：样本在两个聚类边界上
- 接近-1：样本可能被分配到错误的聚类

### 簇内平方和 (Inertia)

- 值越小越好
- 表示样本到其聚类中心的距离平方和
- 用于肘部法则确定最优聚类数

## 最佳实践

1. **数据预处理**
   - 确保数据包含数值列
   - 处理缺失值（会自动填充为0）
   - 考虑数据标准化（如果需要）

2. **选择聚类数**
   - 使用 `find_optimal_clusters` 寻找最优值
   - 结合业务需求确定聚类数
   - 观察轮廓系数和肘部图

3. **特征选择**
   - 选择与业务目标相关的数值特征
   - 避免使用过多无关特征
   - 考虑特征的重要性

4. **结果解释**
   - 分析每个聚类的特征
   - 结合业务场景理解聚类结果
   - 验证聚类的合理性

## 示例代码

查看完整示例：
- [scripts/kmeans_analysis_example.py](../scripts/kmeans_analysis_example.py)

## 参考资源

- [K-means聚类算法：原理、实例与代码分析](https://developer.aliyun.com/article/1541894)
- [scikit-learn K-means文档](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [K-means算法原理](https://en.wikipedia.org/wiki/K-means_clustering)
