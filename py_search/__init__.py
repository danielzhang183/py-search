"""
py_search - K-means聚类分析工具

一个简单易用的Python工具，用于对CSV数据进行K-means聚类分析。
"""

__version__ = "0.1.0"
__author__ = "Dylan Zhang"

# 导入CSV读取工具（K-means分析需要）
from .csv_handler import CSVReader

# 导入数据分析模块
try:
    from .data_analyzer import DataAnalyzer, kmeans_analyze_csv, save_analysis_results
    _has_analyzer = True
except ImportError:
    _has_analyzer = False

# 可选导入可视化模块
try:
    from .visualizer import ClusterVisualizer, visualize_cluster_result
    _has_visualizer = True
except ImportError:
    _has_visualizer = False

# 构建导出列表
__all__ = ["CSVReader"]

if _has_analyzer:
    __all__.extend(["DataAnalyzer", "kmeans_analyze_csv", "save_analysis_results"])

if _has_visualizer and _has_analyzer:
    __all__.extend(["ClusterVisualizer", "visualize_cluster_result"])
