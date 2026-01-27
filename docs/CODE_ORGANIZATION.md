# Python项目代码组织最佳实践

## 工具函数（Utility Functions）的组织方式

### 常见组织模式

#### 1. 单一工具模块（适合小型项目）

```
py_search/
├── utils.py          # 所有工具函数
├── helpers.py        # 辅助函数
└── common.py         # 通用函数
```

**优点：** 简单直接，易于查找  
**缺点：** 文件可能过大，难以维护

#### 2. 按功能分类的工具模块（推荐）

```
py_search/
├── utils/
│   ├── __init__.py
│   ├── text_utils.py      # 文本处理工具
│   ├── file_utils.py      # 文件操作工具
│   ├── data_utils.py      # 数据处理工具
│   └── network_utils.py   # 网络相关工具
```

**优点：** 职责清晰，易于维护和扩展  
**缺点：** 需要更多文件

#### 3. 按领域分类（当前项目采用的方式）

```
py_search/
├── csv_handler.py    # CSV相关（类+便捷函数）
├── data_analyzer.py  # 数据分析（类+便捷函数）
├── web_scraper.py   # 爬虫相关（类+便捷函数）
└── visualizer.py    # 可视化（类+便捷函数）
```

**优点：** 功能内聚，相关代码在一起  
**缺点：** 跨模块的工具函数可能重复

#### 4. 混合模式（最佳实践）

```
py_search/
├── core/              # 核心功能模块
│   ├── csv_handler.py
│   ├── data_analyzer.py
│   └── web_scraper.py
├── utils/             # 通用工具函数
│   ├── __init__.py
│   ├── text.py        # 文本处理
│   ├── file.py        # 文件操作
│   └── validation.py  # 数据验证
└── helpers/           # 辅助功能
    └── formatting.py
```

## 当前项目分析

### 当前组织方式

当前项目采用**按领域分类**的方式：

- `csv_handler.py` - CSV处理（类 + 便捷函数）
- `data_analyzer.py` - 数据分析（类 + 便捷函数）
- `web_scraper.py` - 爬虫（类 + 便捷函数）
- `visualizer.py` - 可视化（类 + 内部工具函数）

### 存在的问题

1. **跨模块工具函数分散**：如 `clean_text`, `extract_emails` 在 `web_scraper.py` 中，但可能被其他模块使用
2. **内部工具函数命名**：`_configure_chinese_font` 使用下划线前缀，表示内部使用
3. **便捷函数位置**：有些便捷函数在模块末尾，有些在类中

## 推荐的重构方案

### 方案1: 创建通用工具模块（推荐）

```
py_search/
├── utils/
│   ├── __init__.py
│   ├── text.py        # 文本处理工具
│   ├── file.py        # 文件操作工具
│   └── validation.py  # 数据验证工具
```

### 方案2: 保持当前结构，但优化组织

- 将跨模块通用的工具函数提取到 `utils.py`
- 模块特定的工具函数保留在原模块
- 使用清晰的命名和文档

## 工具函数分类指南

### 应该放在 utils 中的函数

1. **纯函数**（无副作用，可复用）
   - `clean_text()` - 文本清洗
   - `extract_emails()` - 提取邮箱
   - `extract_numbers()` - 提取数字
   - `normalize_url()` - URL规范化

2. **通用验证函数**
   - `validate_email()`
   - `validate_url()`
   - `is_valid_csv()`

3. **格式化函数**
   - `format_file_size()`
   - `format_timestamp()`

### 应该保留在模块中的函数

1. **模块特定的便捷函数**
   - `kmeans_analyze_csv()` - 数据分析模块特定
   - `scrape_and_save()` - 爬虫模块特定

2. **内部工具函数**（以下划线开头）
   - `_configure_chinese_font()` - 可视化模块内部使用
   - `_run_analysis()` - CLI模块内部使用

## 命名规范

### 便捷函数命名

```python
# 好的命名
def analyze_csv_with_kmeans(...)  # 描述性强
def download_csv_from_url(...)    # 动作明确
def save_analysis_results(...)     # 功能清晰

# 避免的命名
def helper(...)                    # 太泛化
def util(...)                      # 不明确
def do_something(...)              # 不具体
```

### 内部工具函数命名

```python
# 使用下划线前缀表示内部使用
def _configure_chinese_font(...)   # 模块内部
def _validate_input(...)           # 内部验证
def _format_output(...)            # 内部格式化
```

## 导入和导出

### **init**.py 中的组织

```python
# 方式1: 直接导出便捷函数
from .csv_handler import read_csv_files, download_csv_from_url
from .data_analyzer import kmeans_analyze_csv
from .utils.text import clean_text, extract_emails

# 方式2: 通过utils模块导出
from . import utils
# 使用: utils.clean_text()

# 方式3: 分类导出
from .utils.text import *
from .utils.file import *
```

## 实际示例

### 重构前（当前）

```python
# web_scraper.py
def clean_text(text: str) -> str:
    """清洗文本"""
    ...

def extract_emails(text: str) -> List[str]:
    """提取邮箱"""
    ...
```

### 重构后（推荐）

```python
# utils/text.py
def clean_text(text: str) -> str:
    """清洗文本：去除多余空白"""
    ...

def extract_emails(text: str) -> List[str]:
    """从文本中提取邮箱地址"""
    ...

def extract_numbers(text: str) -> List[float]:
    """从文本中提取数字"""
    ...

# utils/__init__.py
from .text import clean_text, extract_emails, extract_numbers
__all__ = ['clean_text', 'extract_emails', 'extract_numbers']

# web_scraper.py
from .utils import clean_text, extract_emails
```

## 最佳实践总结

1. **按功能分类**：相关功能的工具函数放在一起
2. **清晰的命名**：函数名应该清楚表达功能
3. **适当的文档**：每个函数都应该有docstring
4. **避免重复**：提取通用的工具函数到utils模块
5. **保持内聚**：模块特定的函数保留在原模块
6. **统一导出**：通过 `__init__.py` 统一管理导出

## 参考项目结构

### 小型项目（< 10个工具函数）

```
utils.py  # 单一文件即可
```

### 中型项目（10-50个工具函数）

```
utils/
├── __init__.py
├── text.py
├── file.py
└── validation.py
```

### 大型项目（> 50个工具函数）

```
utils/
├── __init__.py
├── text/
│   ├── __init__.py
│   ├── cleaning.py
│   └── extraction.py
├── file/
│   ├── __init__.py
│   ├── io.py
│   └── format.py
└── validation/
    ├── __init__.py
    └── validators.py
```
