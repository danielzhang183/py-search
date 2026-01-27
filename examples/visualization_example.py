#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚类结果可视化示例

演示如何使用py_search对K-means聚类结果进行可视化
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_search import CSVReader
from py_search.data_analyzer import kmeans_analyze_csv
from py_search.visualizer import ClusterVisualizer, visualize_cluster_result


def example_basic_visualization():
    """示例1: 基本可视化"""
    print("=" * 60)
    print("示例1: 基本可视化")
    print("=" * 60)
    
    try:
        # 执行聚类分析
        result = kmeans_analyze_csv(
            csv_file="customer_data.csv",
            n_clusters=4,
            directory="./data"
        )
        
        # 生成可视化图表
        saved_images = visualize_cluster_result(result, "customer_data.csv")
        
        print(f"\n✓ 可视化完成！生成的图表:")
        for chart_type, path in saved_images.items():
            print(f"  - {chart_type}: {path}")
        
    except ImportError as e:
        print(f"✗ 错误: {e}")
        print("\n提示: 请安装matplotlib: pip install matplotlib")
    except Exception as e:
        print(f"✗ 错误: {e}")


def example_custom_visualization():
    """示例2: 自定义可视化"""
    print("\n" + "=" * 60)
    print("示例2: 自定义可视化")
    print("=" * 60)
    
    try:
        # 读取数据
        reader = CSVReader(directory="./data")
        df = reader.read_with_pandas("customer_data.csv")
        
        # 执行分析
        result = kmeans_analyze_csv(
            csv_file="customer_data.csv",
            n_clusters=4,
            directory="./data"
        )
        
        # 创建可视化器
        visualizer = ClusterVisualizer()
        
        # 提取数据
        data = df[result['used_columns']].values
        labels = result['cluster_result']['labels']
        centers = result['cluster_result']['centers']
        
        # 生成2D图
        path_2d = visualizer.plot_2d_clusters(
            data, labels, centers, result['used_columns'],
            title="客户数据聚类分析 (2D)"
        )
        print(f"✓ 2D图已保存: {path_2d}")
        
        # 生成3D图（如果有3个或更多特征）
        if data.shape[1] >= 3:
            path_3d = visualizer.plot_3d_clusters(
                data, labels, centers, result['used_columns'],
                title="客户数据聚类分析 (3D)"
            )
            print(f"✓ 3D图已保存: {path_3d}")
        
        # 生成分布图
        path_dist = visualizer.plot_cluster_distribution(
            result['cluster_result']['cluster_counts'],
            title="客户聚类分布"
        )
        print(f"✓ 分布图已保存: {path_dist}")
        
    except Exception as e:
        print(f"✗ 错误: {e}")


def example_optimal_clusters_visualization():
    """示例3: 最优聚类数可视化"""
    print("\n" + "=" * 60)
    print("示例3: 最优聚类数可视化")
    print("=" * 60)
    
    try:
        from py_search.data_analyzer import DataAnalyzer
        
        # 读取数据
        reader = CSVReader(directory="./data")
        df = reader.read_with_pandas("customer_data.csv")
        
        # 数据预处理
        analyzer = DataAnalyzer()
        data, columns = analyzer.preprocess_data(df)
        
        # 寻找最优聚类数
        optimal_result = analyzer.find_optimal_clusters(data, max_clusters=10)
        
        print(f"最优聚类数: {optimal_result['optimal_k']}")
        
        # 创建可视化器
        visualizer = ClusterVisualizer()
        
        # 生成肘部法则图
        elbow_path = visualizer.plot_elbow_method(
            optimal_result['k_range'],
            optimal_result['inertias'],
            optimal_k=optimal_result['optimal_k'],
            title="肘部法则 - 客户数据"
        )
        print(f"✓ 肘部法则图已保存: {elbow_path}")
        
        # 生成轮廓系数图
        silhouette_path = visualizer.plot_silhouette_scores(
            optimal_result['k_range'],
            optimal_result['silhouette_scores'],
            optimal_k=optimal_result['optimal_k'],
            title="轮廓系数分析 - 客户数据"
        )
        print(f"✓ 轮廓系数图已保存: {silhouette_path}")
        
    except Exception as e:
        print(f"✗ 错误: {e}")


if __name__ == "__main__":
    print("聚类结果可视化示例\n")
    
    # 运行示例
    example_basic_visualization()
    example_custom_visualization()
    example_optimal_clusters_visualization()
    
    print("\n" + "=" * 60)
    print("安装依赖:")
    print("  pip install matplotlib pandas scikit-learn numpy")
    print("=" * 60)
