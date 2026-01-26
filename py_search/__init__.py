"""
py_search - Python CSV文件读取工具

一个简单易用的Python工具，用于读取和处理CSV文件。
"""

__version__ = "0.1.0"
__author__ = "Dylan Zhang"

from .csv_handler import CSVReader, read_csv_files, read_csv_simple, download_csv_from_url

# 可选导入Coze集成模块
try:
    from .coze_integration import CozeClient, create_coze_client_from_env
    _has_coze = True
except ImportError:
    _has_coze = False

# 可选导入数据分析模块
try:
    from .data_analyzer import DataAnalyzer, kmeans_analyze_csv
    _has_analyzer = True
except ImportError:
    _has_analyzer = False

# 构建导出列表
__all__ = [
    "CSVReader", 
    "read_csv_files", 
    "read_csv_simple", 
    "download_csv_from_url"
]

if _has_coze:
    __all__.extend(["CozeClient", "create_coze_client_from_env"])

if _has_analyzer:
    __all__.extend(["DataAnalyzer", "kmeans_analyze_csv", "save_analysis_results"])
