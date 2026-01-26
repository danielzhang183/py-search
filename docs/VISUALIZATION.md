# 聚类结果可视化指南

## 简介

项目提供了完整的可视化功能，可以直观地展示K-means聚类结果，帮助理解数据分布和聚类效果。

## 安装依赖

```bash
pip install matplotlib
```

或者安装所有依赖：

```bash
pip install -r requirements.txt
```

## 可视化图表类型

### 1. 2D散点图

展示前两个特征的聚类分布，每个聚类用不同颜色表示，聚类中心用红色X标记。

```python
from py_search.visualizer import ClusterVisualizer

visualizer = ClusterVisualizer()
path = visualizer.plot_2d_clusters(
    data, labels, centers, feature_names,
    title="K-means聚类结果 (2D)"
)
```

### 2. 3D散点图

展示前三个特征的聚类分布，提供更立体的视角。

```python
path = visualizer.plot_3d_clusters(
    data, labels, centers, feature_names,
    title="K-means聚类结果 (3D)"
)
```

### 3. 聚类分布统计图

柱状图展示每个聚类的样本数量。

```python
path = visualizer.plot_cluster_distribution(
    cluster_counts,
    title="聚类分布统计"
)
```

### 4. 肘部法则图

用于寻找最优聚类数，展示不同k值下的簇内平方和。

```python
path = visualizer.plot_elbow_method(
    k_range, inertias, optimal_k=4,
    title="肘部法则 - 寻找最优聚类数"
)
```

### 5. 轮廓系数图

展示不同k值下的轮廓系数，帮助评估聚类质量。

```python
path = visualizer.plot_silhouette_scores(
    k_range, scores, optimal_k=4,
    title="轮廓系数分析"
)
```

## 使用方式

### 方式1: 命令行自动生成

运行分析时，会自动生成可视化图表：

```bash
# 基本分析（自动生成可视化）
python3 -m py_search.cli --analysis customer_data.csv --dir examples --clusters 4

# 不生成可视化图表
python3 -m py_search.cli --analysis customer_data.csv --dir examples --clusters 4 --no-viz

# 寻找最优聚类数（会生成肘部法则图和轮廓系数图）
python3 -m py_search.cli --analysis customer_data.csv --dir examples --optimal
```

### 方式2: Python代码中使用

#### 完整可视化

```python
from py_search.data_analyzer import kmeans_analyze_csv
from py_search.visualizer import visualize_cluster_result

# 执行分析
result = kmeans_analyze_csv(
    csv_file="customer_data.csv",
    n_clusters=4,
    directory="./examples"
)

# 生成所有可视化图表
saved_images = visualize_cluster_result(result, "customer_data.csv")

print("生成的图表:")
for chart_type, path in saved_images.items():
    print(f"  {chart_type}: {path}")
```

#### 自定义可视化

```python
from py_search.visualizer import ClusterVisualizer
from py_search import CSVReader
from py_search.data_analyzer import DataAnalyzer, kmeans_analyze_csv

# 执行分析
result = kmeans_analyze_csv("customer_data.csv", n_clusters=4, directory="./examples")

# 创建可视化器
visualizer = ClusterVisualizer()

# 提取数据
df = result['dataframe']
data = df[result['used_columns']].values
labels = result['cluster_result']['labels']
centers = result['cluster_result']['centers']

# 生成2D图
path_2d = visualizer.plot_2d_clusters(
    data, labels, centers, result['used_columns'],
    title="客户数据聚类分析"
)

# 生成3D图（如果有3个或更多特征）
if data.shape[1] >= 3:
    path_3d = visualizer.plot_3d_clusters(
        data, labels, centers, result['used_columns'],
        title="客户数据聚类分析 (3D)"
    )

# 生成分布图
path_dist = visualizer.plot_cluster_distribution(
    result['cluster_result']['cluster_counts'],
    title="客户聚类分布"
)
```

#### 最优聚类数可视化

```python
from py_search.data_analyzer import DataAnalyzer
from py_search.visualizer import ClusterVisualizer
from py_search import CSVReader

# 读取数据
reader = CSVReader(directory="./examples")
df = reader.read_with_pandas("customer_data.csv")

# 数据预处理
analyzer = DataAnalyzer()
data, columns = analyzer.preprocess_data(df)

# 寻找最优聚类数
optimal_result = analyzer.find_optimal_clusters(data, max_clusters=10)

# 创建可视化器
visualizer = ClusterVisualizer()

# 生成肘部法则图
elbow_path = visualizer.plot_elbow_method(
    optimal_result['k_range'],
    optimal_result['inertias'],
    optimal_k=optimal_result['optimal_k'],
    title="肘部法则 - 客户数据"
)

# 生成轮廓系数图
silhouette_path = visualizer.plot_silhouette_scores(
    optimal_result['k_range'],
    optimal_result['silhouette_scores'],
    optimal_k=optimal_result['optimal_k'],
    title="轮廓系数分析 - 客户数据"
)
```

## 图表保存位置

所有可视化图表默认保存在 `reports/` 文件夹下，文件名格式：
- `{原文件名}_2d_{时间戳}.png` - 2D散点图
- `{原文件名}_3d_{时间戳}.png` - 3D散点图
- `{原文件名}_distribution_{时间戳}.png` - 分布图
- `elbow_method_{时间戳}.png` - 肘部法则图
- `silhouette_scores_{时间戳}.png` - 轮廓系数图

## 图表解读

### 2D/3D散点图
- **不同颜色**：代表不同的聚类
- **红色X**：表示聚类中心
- **点之间的距离**：距离越近，特征越相似

### 聚类分布图
- **柱状高度**：表示每个聚类的样本数量
- **平衡性**：各聚类样本数越接近，分布越均匀

### 肘部法则图
- **下降趋势**：k值增加，簇内平方和减小
- **肘部点**：下降趋势明显变缓的点，通常是最优k值

### 轮廓系数图
- **数值范围**：-1 到 1
- **越大越好**：接近1表示聚类效果很好
- **最优k值**：轮廓系数最高的k值

## 最佳实践

1. **特征选择**：选择2-3个最重要的特征进行可视化，避免维度过多
2. **颜色区分**：确保有足够的颜色区分不同聚类
3. **图表标题**：使用描述性的标题，包含数据来源和聚类数
4. **保存格式**：使用PNG格式（300 DPI）确保清晰度
5. **对比分析**：生成多个k值的图表进行对比

## 示例代码

查看完整示例：
- [scripts/visualization_example.py](../scripts/visualization_example.py)

## 故障排除

### matplotlib未安装

**错误信息：** `ModuleNotFoundError: No module named 'matplotlib'`

**解决方案：**
```bash
pip install matplotlib
```

### 图表无法显示

如果需要在Jupyter Notebook中显示图表，使用：

```python
import matplotlib.pyplot as plt
%matplotlib inline
```

### 中文显示问题

**自动配置：** 项目已自动配置中文字体支持，无需手动设置。

如果仍然遇到中文显示问题（显示为方块或警告），可以手动指定字体：

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 查看系统可用的中文字体
fonts = [f.name for f in fm.fontManager.ttflist if 'Chinese' in f.name or 'CJK' in f.name]
print('可用的中文字体:', fonts)

# 手动配置（macOS）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC']
plt.rcParams['axes.unicode_minus'] = False

# 手动配置（Windows）
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
# plt.rcParams['axes.unicode_minus'] = False

# 手动配置（Linux）
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC']
# plt.rcParams['axes.unicode_minus'] = False
```

**macOS字体路径：**
- Arial Unicode MS: `/System/Library/Fonts/Supplemental/Arial Unicode.ttf`
- PingFang SC: `/System/Library/Fonts/PingFang.ttc`
- Heiti SC: `/System/Library/Fonts/STHeiti Medium.ttc`

## 参考资源

- [matplotlib官方文档](https://matplotlib.org/)
- [K-means可视化最佳实践](https://scikit-learn.org/stable/modules/clustering.html#k-means)
