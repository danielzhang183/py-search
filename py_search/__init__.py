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
    __all__ = [
        "CSVReader", 
        "read_csv_files", 
        "read_csv_simple", 
        "download_csv_from_url",
        "CozeClient",
        "create_coze_client_from_env"
    ]
except ImportError:
    # 如果cozepy未安装，不导出Coze相关类
    __all__ = [
        "CSVReader", 
        "read_csv_files", 
        "read_csv_simple", 
        "download_csv_from_url"
    ]
