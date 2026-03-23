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

### 作为包安装（推荐）

1. 克隆或下载项目到本地
2. 安装项目：

```bash
pip install -e .
```

或者安装到系统：

```bash
pip install .
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

## 许可证

MIT License

## 参考

- [K-means聚类算法：原理、实例与代码分析](https://developer.aliyun.com/article/1541894)
