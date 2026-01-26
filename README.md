# py-search

一个简单易用的Python工具，用于读取和处理CSV文件。

## 功能特性

- 🔍 自动扫描指定文件夹下的所有CSV文件
- 📊 支持两种读取方式：标准库版本和pandas版本
- 📝 显示CSV文件的基本信息（行数、列数、列名等）
- 🌐 支持从HTTPS URL下载CSV文件
- 💾 自动保存下载的文件到examples文件夹
- 🤖 集成Coze AI平台，支持AI分析
- 📈 **K-means聚类分析**（参考[阿里云文章](https://developer.aliyun.com/article/1541894)）
- 📊 **可视化展示**：自动生成2D/3D散点图、分布图、肘部法则图等
- 🛡️ 包含完善的错误处理机制
- 📦 标准化的Python项目结构
- 🧪 包含单元测试

## 项目结构

```scss
py-search/
├── py_search/              # 主包目录
│   ├── __init__.py         # 包初始化文件
│   ├── csv_handler.py      # CSV处理核心模块（读取、下载）
│   ├── data_analyzer.py    # 数据分析模块（K-means聚类）
│   ├── coze_integration.py # Coze AI集成模块
│   └── cli.py              # 命令行接口
├── tests/                  # 测试目录
│   ├── __init__.py
│   └── test_csv_handler.py # 单元测试
├── examples/               # 示例数据目录（仅存放CSV数据文件）
│   └── example.csv         # 示例CSV文件
├── reports/                 # 分析报告目录（自动生成）
│   ├── *_clustered_*.csv   # 带聚类标签的CSV文件
│   ├── *_report_*.json     # 分析报告（JSON格式）
│   └── *_report_*.txt      # 分析报告（文本格式）
├── scripts/                # 示例脚本目录
│   ├── download_example.py # 下载功能使用示例
│   ├── coze_integration_example.py # Coze API集成示例
│   └── kmeans_analysis_example.py # K-means聚类分析示例
├── docs/                   # 文档目录
│   └── COZE_INTEGRATION.md # Coze集成指南
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

1. 使用Python模块方式运行：

```bash
python3 -m py_search.cli
```

## 使用方法

### 命令行使用

安装后可以使用命令行工具：

```bash
# 读取当前目录下所有CSV文件（使用pandas）
py-search

# 使用标准库读取（不需要pandas）
py-search --simple

# 读取指定文件
py-search --file example.csv

# 读取指定目录下的CSV文件
py-search --dir /path/to/directory

# 从HTTPS URL下载CSV文件到examples文件夹
py-search --download https://example.com/data.csv

# 下载并指定文件名
py-search --download https://example.com/data.csv --filename mydata.csv

# 对CSV文件进行K-means聚类分析
py-search --analysis customer_data.csv --dir examples

# 指定聚类数为4
py-search --analysis customer_data.csv --clusters 4 --dir examples

# 指定使用的列
py-search --analysis customer_data.csv --columns 消费金额 购买次数 --dir examples

# 自动寻找最优聚类数
py-search --analysis customer_data.csv --optimal --dir examples

# 注意：分析结果会自动保存到 reports/ 文件夹
# - *_clustered_*.csv: 包含聚类标签的完整数据
# - *_report_*.json: 分析报告（JSON格式）
# - *_report_*.txt: 分析报告（文本格式）
# - *_2d_*.png, *_3d_*.png: 可视化图表（如果安装了matplotlib）
# - --no-viz: 不生成可视化图表
```

### Python代码中使用

#### 方式1：使用类

```python
from py_search import CSVReader

# 创建读取器实例
reader = CSVReader(directory="./examples")

# 查找所有CSV文件
csv_files = reader.find_csv_files()
print(f"找到 {len(csv_files)} 个CSV文件")

# 使用标准库读取
rows = reader.read_with_standard_lib("example.csv")
for row in rows:
    print(row)

# 使用pandas读取（需要安装pandas）
df = reader.read_with_pandas("example.csv")
print(df.head())

# 获取文件信息
info = reader.get_file_info("example.csv")
print(f"行数: {info['rows']}, 列数: {info['columns']}")
```

#### 方式2：使用函数

```python
from py_search import read_csv_files, read_csv_simple, download_csv_from_url

# 读取目录下所有CSV文件
read_csv_files(directory="./examples", use_pandas=True)

# 读取指定文件（使用标准库）
read_csv_simple("example.csv", directory="./examples")

# 从URL下载CSV文件到examples文件夹
save_path = download_csv_from_url("https://example.com/data.csv")
print(f"文件已保存到: {save_path}")

# 下载并指定文件名和目录
save_path = download_csv_from_url(
    "https://example.com/data.csv",
    save_directory="./examples",
    filename="mydata.csv"
)
```

#### 方式3：使用类的下载方法

```python
from py_search import CSVReader

# 创建读取器实例，指定保存目录
reader = CSVReader(directory="./examples")

# 下载CSV文件
save_path = reader.download_csv("https://example.com/data.csv", filename="data.csv")
print(f"文件已保存到: {save_path}")
```

## 开发

### 运行测试

项目使用 Python 标准库的 `unittest` 框架，无需安装额外依赖：

```bash
# 运行所有测试（使用标准库 unittest）
python3 -m unittest discover tests

# 或者直接运行测试文件
python3 -m unittest tests.test_csv_handler

# 或者使用 pytest（需要先安装：pip install pytest）
python3 -m pytest tests/

# 使用 pytest 并显示覆盖率（需要安装：pip install pytest pytest-cov）
python3 -m pytest --cov=py_search tests/
```

### 安装开发依赖

如果需要使用 pytest 进行测试：

```bash
# 安装开发依赖（包括 pytest）
pip3 install -r requirements-dev.txt

# 或者使用 setup.py 安装
pip3 install -e ".[dev]"
```

## 系统要求

- Python 3.6+（在 macOS 上使用 `python3` 命令）
- **必需依赖：**
  - pandas >= 2.0.0（用于CSV读取和数据分析）
  - scikit-learn >= 1.0.0（用于K-means聚类）
  - numpy >= 1.20.0（用于数值计算）
  - matplotlib >= 3.5.0（用于可视化，可选但推荐）
- **可选依赖：**
  - cozepy（用于Coze AI集成）

**注意**：在 macOS 和大多数 Linux 系统上，Python 3 的命令是 `python3` 而不是 `python`。如果遇到 `command not found: python` 错误，请使用 `python3` 替代。

## 注意事项

- 脚本会自动处理UTF-8编码的CSV文件
- 如果文件夹下没有CSV文件，脚本会提示相应信息
- 如果CSV文件读取失败，会显示错误信息但不会中断程序
- 使用pandas功能需要先安装pandas：`pip install pandas`
- 下载功能使用Python标准库，无需额外依赖
- 下载的文件默认保存到 `examples/` 文件夹
- 如果URL中没有文件名，会自动生成一个基于域名的文件名

## 许可证

MIT License

## 扩展功能

### K-means聚类分析

项目支持对CSV数据进行K-means聚类分析，参考[阿里云开发者社区文章](https://developer.aliyun.com/article/1541894)。

**分析结果会自动保存到 `reports/` 文件夹：**
- `*_clustered_*.csv` - 包含原始数据和聚类标签的CSV文件
- `*_report_*.json` - 分析报告（JSON格式，包含统计信息）
- `*_report_*.txt` - 分析报告（文本格式，更易读）

**快速开始：**

```python
from py_search import CSVReader
from py_search.data_analyzer import DataAnalyzer, kmeans_analyze_csv

# 方式1: 使用便捷函数
result = kmeans_analyze_csv(
    csv_file="example.csv",
    n_clusters=3,  # 分为3个聚类
    directory="./examples"
)

# 查看结果
print(f"聚类数: {result['n_clusters']}")
print(f"各聚类样本数: {result['cluster_info']}")

# 方式2: 使用类方法
reader = CSVReader(directory="./examples")
df = reader.read_with_pandas("example.csv")

analyzer = DataAnalyzer()
data, columns = analyzer.preprocess_data(df)
result = analyzer.kmeans_cluster(data, n_clusters=3)

# 寻找最优聚类数
optimal = analyzer.find_optimal_clusters(data, max_clusters=10)
print(f"最优聚类数: {optimal['optimal_k']}")
```

**客户细分示例：**

```python
# 对客户数据进行细分
result = kmeans_analyze_csv(
    csv_file="customer_data.csv",
    n_clusters=4,  # 将客户分为4类
    numeric_columns=["消费金额", "购买次数", "最近购买天数"],
    directory="./examples"
)

# 查看每个客户所属的聚类
df = result['dataframe']
print(df[['客户ID', 'cluster']])
```

**安装依赖：**

```bash
pip install pandas scikit-learn numpy
```

**示例代码：**

- 查看 [scripts/kmeans_analysis_example.py](scripts/kmeans_analysis_example.py) 获取完整示例

### Coze API 集成

项目已内置 Coze（扣子）AI平台集成模块，可以使用AI Bot分析CSV数据。

**使用方式：**

```python
from py_search import CSVReader
from py_search.coze_integration import CozeClient, create_coze_client_from_env

# 方式1: 从环境变量创建客户端（推荐）
client = create_coze_client_from_env()

# 方式2: 手动创建客户端
client = CozeClient(access_token="your_pat_token")

# 分析CSV文件
reader = CSVReader(directory="./examples")
info = reader.get_file_info("example.csv")

# 使用Coze Bot分析
result = client.analyze_csv_data(
    bot_id="your_bot_id",
    user_id="user_123",
    csv_summary=f"行数: {info['rows']}, 列数: {info['columns']}",
    question="这个数据集有什么特点？"
)
print(result)
```

**环境变量配置：**

```bash
export COZE_ACCESS_TOKEN="your_pat_token"
export COZE_BOT_ID="your_bot_id"
```

**详细文档：**

- 集成指南: [docs/COZE_INTEGRATION.md](docs/COZE_INTEGRATION.md)
- 示例代码: [scripts/coze_integration_example.py](scripts/coze_integration_example.py)

**安装依赖：**

```bash
pip3 install cozepy
```

## 故障排除

如果遇到问题，请查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 获取详细解决方案。

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v0.1.0

- 初始版本
- 支持标准库和pandas两种读取方式
- 提供命令行接口
- 包含单元测试
