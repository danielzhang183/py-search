"""
py_search - Python CSV文件读取工具

一个简单易用的Python工具，用于读取和处理CSV文件。
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .csv_handler import CSVReader, read_csv_files, read_csv_simple, download_csv_from_url

__all__ = ["CSVReader", "read_csv_files", "read_csv_simple", "download_csv_from_url"]
