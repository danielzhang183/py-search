# py-search

一个简单易用的Python工具，用于对CSV数据进行K-means聚类分析。

## 功能特性

- 📈 **K-means聚类分析**（参考[阿里云文章](https://developer.aliyun.com/article/1541894)）
- 📊 **可视化展示**：自动生成2D/3D散点图、分布图、肘部法则图等
- 🔍 **自动寻找最优聚类数**：使用肘部法则和轮廓系数
- 💾 **自动保存分析结果**：CSV、JSON、文本报告
- 🛡️ 包含完善的错误处理机制
- 📦 标准化的Python项目结构
- 🧪 包含单元测试

## 项目结构

```scss
py-search/
├── py_search/              # 主包目录
│   ├── __init__.py         # 包初始化文件
│   ├── csv_handler.py      # CSV读取模块
│   ├── data_analyzer.py    # K-means聚类分析模块
│   ├── visualizer.py       # 可视化模块
│   └── cli.py              # 命令行接口
├── reports/                # 分析报告目录（自动生成）
│   ├── *_clustered_*.csv   # 带聚类标签的CSV文件
│   ├── *_report_*.json     # 分析报告（JSON格式）
│   └── *_report_*.txt      # 分析报告（文本格式）
├── README.md               # 项目说明文档
├── requirements.txt        # 项目依赖
├── setup.py               # 安装配置文件
└── .gitignore             # Git忽略文件
```

## 安装

### 方法1：作为包安装（推荐）

1. 克隆或下载项目到本地
2. 安装项目：

```bash
pip install -e .
```

或者安装到系统：

```bash
pip install .
```

### 方法2：直接使用（开发模式）

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 使用Python模块方式运行：

```bash
python3 -m py_search.cli --analysis customer_data.csv --dir data
```

## 使用方法

### 命令行使用

安装后可以使用命令行工具：

```bash
# 基本K-means聚类分析（默认3个聚类）
py-search --analysis customer_data.csv --dir data

# 指定聚类数
py-search --analysis customer_data.csv --dir data --clusters 4

# 指定使用的列
py-search --analysis customer_data.csv --dir data --columns 消费金额 购买次数 最近购买天数

# 自动寻找最优聚类数
py-search --analysis customer_data.csv --dir data --optimal

# 不生成可视化图表
py-search --analysis customer_data.csv --dir data --clusters 4 --no-viz
```

### Python API使用

**方式1: 使用便捷函数**

```python
from py_search.data_analyzer import kmeans_analyze_csv

# 对CSV文件进行聚类分析
result = kmeans_analyze_csv(
    csv_file="customer_data.csv",
    n_clusters=4,  # 分为4个聚类
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

**方式2: 使用类方法**

```python
from py_search import CSVReader
from py_search.data_analyzer import DataAnalyzer

# 读取CSV文件
reader = CSVReader(directory="./data")
df = reader.read_with_pandas("customer_data.csv")

# 创建分析器
analyzer = DataAnalyzer()

# 数据预处理
data, columns = analyzer.preprocess_data(df)

# 执行聚类
result = analyzer.kmeans_cluster(data, n_clusters=4)

# 查看结果
print(f"聚类标签: {result['labels']}")
print(f"聚类中心: {result['centers']}")
print(f"轮廓系数: {result['silhouette_score']}")
```

**寻找最优聚类数**

```python
from py_search import CSVReader
from py_search.data_analyzer import DataAnalyzer

reader = CSVReader(directory="./data")
df = reader.read_with_pandas("customer_data.csv")

analyzer = DataAnalyzer()
data, _ = analyzer.preprocess_data(df)

# 寻找最优聚类数（测试2-10个聚类）
optimal = analyzer.find_optimal_clusters(data, max_clusters=10)
print(f"最优聚类数: {optimal['optimal_k']}")
print(f"轮廓系数: {optimal['silhouette_scores']}")
```

**可视化**

```python
from py_search.visualizer import visualize_cluster_result

# 自动生成所有可视化图表
saved_images = visualize_cluster_result(
    result=result,
    original_file="customer_data.csv"
)

print("生成的图表:")
for chart_type, path in saved_images.items():
    print(f"  - {chart_type}: {path}")
```

## 分析结果

运行分析后，结果会自动保存到 `reports/` 目录：

- `*_clustered_*.csv` - 包含原始数据和聚类标签的CSV文件
- `*_report_*.json` - 分析报告（JSON格式，包含统计信息）
- `*_report_*.txt` - 分析报告（文本格式，更易读）
- `*_2d_clusters.png` - 2D散点图
- `*_3d_clusters.png` - 3D散点图（如果数据有3个或更多特征）
- `*_cluster_distribution.png` - 聚类分布统计图
- `*_elbow_method.png` - 肘部法则图（如果使用--optimal）
- `*_silhouette_scores.png` - 轮廓系数图（如果使用--optimal）

## 客户细分示例

```python
# 对客户数据进行细分
result = kmeans_analyze_csv(
    csv_file="customer_data.csv",
    n_clusters=4,  # 将客户分为4类
    numeric_columns=["消费金额", "购买次数", "最近购买天数"],
    directory="./data"
)

# 查看每个客户所属的聚类
df = result['dataframe']
print(df[['客户ID', 'cluster']])
```

## 依赖

### 必需依赖

```bash
pip install pandas scikit-learn numpy
```

### 可选依赖（可视化）

```bash
pip install matplotlib
```

或者安装所有依赖：

```bash
pip install -r requirements.txt
```

## 文档

- **K-means分析指南**: [docs/KMEANS_ANALYSIS.md](docs/KMEANS_ANALYSIS.md)
- **可视化指南**: [docs/VISUALIZATION.md](docs/VISUALIZATION.md)

## 示例代码

- **K-means分析示例**: [examples/kmeans_analysis_example.py](examples/kmeans_analysis_example.py)
- **可视化示例**: [examples/visualization_example.py](examples/visualization_example.py)

## 开发

### 运行测试

项目使用 Python 标准库的 `unittest` 框架，无需安装额外依赖：

```bash
# 运行所有测试（使用标准库 unittest）
python3 -m unittest discover tests

# 或者直接运行测试文件
python3 -m unittest tests.test_csv_handler
```

### 安装开发依赖

如果需要使用 pytest：

```bash
pip install -r requirements-dev.txt
```

## 许可证

MIT License

## 作者

Dylan Zhang

## 参考

- [K-means聚类算法：原理、实例与代码分析](https://developer.aliyun.com/article/1541894)
