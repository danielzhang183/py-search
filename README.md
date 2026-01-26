# py-search

一个简单易用的Python工具，用于读取和处理CSV文件。

## 功能特性

- 🔍 自动扫描指定文件夹下的所有CSV文件
- 📊 支持两种读取方式：标准库版本和pandas版本
- 📝 显示CSV文件的基本信息（行数、列数、列名等）
- 🛡️ 包含完善的错误处理机制
- 🌐 支持UTF-8编码
- 📦 标准化的Python项目结构
- 🧪 包含单元测试

## 项目结构

```
py-search/
├── py_search/              # 主包目录
│   ├── __init__.py         # 包初始化文件
│   ├── csv_reader.py       # CSV读取核心模块
│   └── cli.py              # 命令行接口
├── tests/                  # 测试目录
│   ├── __init__.py
│   └── test_csv_reader.py  # 单元测试
├── examples/               # 示例数据
│   └── example.csv         # 示例CSV文件
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
python -m py_search.cli
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
from py_search import read_csv_files, read_csv_simple

# 读取目录下所有CSV文件
read_csv_files(directory="./examples", use_pandas=True)

# 读取指定文件（使用标准库）
read_csv_simple("example.csv", directory="./examples")
```

## 开发

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行测试并显示覆盖率
pytest --cov=py_search tests/
```

### 开发模式安装

```bash
pip install -e ".[dev]"
```

## 系统要求

- Python 3.6+
- （可选）pandas >= 2.0.0（用于完整功能）

## 注意事项

- 脚本会自动处理UTF-8编码的CSV文件
- 如果文件夹下没有CSV文件，脚本会提示相应信息
- 如果CSV文件读取失败，会显示错误信息但不会中断程序
- 使用pandas功能需要先安装pandas：`pip install pandas`

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v0.1.0
- 初始版本
- 支持标准库和pandas两种读取方式
- 提供命令行接口
- 包含单元测试
