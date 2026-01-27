#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K-means聚类分析示例

参考：https://developer.aliyun.com/article/1541894
演示如何使用py_search对CSV数据进行K-means聚类分析
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_search import CSVReader
from py_search.data_analyzer import DataAnalyzer, kmeans_analyze_csv


def example_basic_clustering():
    """示例1: 基本K-means聚类"""
    print("=" * 60)
    print("示例1: 基本K-means聚类分析")
    print("=" * 60)
    
    try:
        # 读取CSV文件
        reader = CSVReader(directory="./data")
        df = reader.read_with_pandas("example.csv")
        
        print(f"\n原始数据:")
        print(df.head())
        print(f"\n数据形状: {df.shape}")
        print(f"数值列: {df.select_dtypes(include=['number']).columns.tolist()}")
        
        # 创建分析器
        analyzer = DataAnalyzer()
        
        # 数据预处理
        data, numeric_columns = analyzer.preprocess_data(df)
        print(f"\n使用的数值列: {numeric_columns}")
        print(f"预处理后数据形状: {data.shape}")
        
        # 执行K-means聚类（3个聚类）
        result = analyzer.kmeans_cluster(data, n_clusters=3)
        
        print(f"\n聚类结果:")
        print(f"- 聚类数量: {result['n_clusters']}")
        print(f"- 每个聚类的样本数: {result['cluster_counts']}")
        print(f"- 轮廓系数: {result['silhouette_score']:.4f}" if result['silhouette_score'] else "- 轮廓系数: 无法计算")
        print(f"- 簇内平方和: {result['inertia']:.2f}")
        
        # 将聚类结果添加到数据框
        df['cluster'] = result['labels']
        print(f"\n添加聚类标签后的数据:")
        print(df.head())
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        print("\n提示:")
        print("1. 确保已安装pandas: pip install pandas")
        print("2. 确保已安装scikit-learn: pip install scikit-learn")
        print("3. 确保examples/example.csv文件存在")


def example_find_optimal_clusters():
    """示例2: 寻找最优聚类数"""
    print("\n" + "=" * 60)
    print("示例2: 寻找最优聚类数（肘部法则）")
    print("=" * 60)
    
    try:
        reader = CSVReader(directory="./data")
        df = reader.read_with_pandas("example.csv")
        
        analyzer = DataAnalyzer()
        data, _ = analyzer.preprocess_data(df)
        
        # 寻找最优聚类数
        optimal_result = analyzer.find_optimal_clusters(data, max_clusters=5)
        
        print(f"\n最优聚类数: {optimal_result['optimal_k']}")
        print(f"\n各聚类数的轮廓系数:")
        for k, score in zip(optimal_result['k_range'], optimal_result['silhouette_scores']):
            marker = " ← 最优" if k == optimal_result['optimal_k'] else ""
            print(f"  k={k}: {score:.4f}{marker}")
        
    except Exception as e:
        print(f"✗ 错误: {e}")


def example_analyze_csv_file():
    """示例3: 使用便捷函数分析CSV文件"""
    print("\n" + "=" * 60)
    print("示例3: 使用便捷函数分析CSV文件")
    print("=" * 60)
    
    try:
        # 使用便捷函数
        result = kmeans_analyze_csv(
            csv_file="example.csv",
            n_clusters=3,
            directory="./data"
        )
        
        print(f"\n分析结果:")
        print(f"- 文件: {result['file']}")
        print(f"- 总样本数: {result['total_samples']}")
        print(f"- 聚类数: {result['n_clusters']}")
        print(f"- 使用的列: {result['used_columns']}")
        
        print(f"\n各聚类统计:")
        for cluster_id, info in result['cluster_info'].items():
            print(f"\n聚类 {cluster_id}:")
            print(f"  - 样本数: {info['count']}")
            if info['mean']:
                print(f"  - 平均值:")
                for col, val in info['mean'].items():
                    print(f"      {col}: {val:.2f}")
        
        print(f"\n聚类质量指标:")
        cr = result['cluster_result']
        print(f"  - 轮廓系数: {cr['silhouette_score']:.4f}" if cr['silhouette_score'] else "  - 轮廓系数: 无法计算")
        print(f"  - 簇内平方和: {cr['inertia']:.2f}")
        
    except Exception as e:
        print(f"✗ 错误: {e}")


def example_customer_segmentation():
    """示例4: 客户细分（参考阿里云文章）"""
    print("\n" + "=" * 60)
    print("示例4: 客户细分分析（参考阿里云文章）")
    print("=" * 60)
    
    print("""
参考文章: https://developer.aliyun.com/article/1541894

典型的客户细分场景：
1. 使用客户的消费金额、购买频率等数值特征
2. 进行K-means聚类，将客户分为不同群体
3. 分析每个群体的特征，制定营销策略

示例数据应包含：
- 客户ID
- 消费金额（数值）
- 购买次数（数值）
- 最近购买时间（可转换为数值）

使用方式：
    result = kmeans_analyze_csv(
        csv_file="customer_data.csv",
        n_clusters=4,  # 将客户分为4类
        numeric_columns=["消费金额", "购买次数", "最近购买天数"],
        directory="./data"
    )
    
    # 查看每个客户所属的聚类
    df = result['dataframe']
    print(df[['客户ID', 'cluster']])
    """)


if __name__ == "__main__":
    print("K-means聚类分析示例\n")
    print("参考文章: https://developer.aliyun.com/article/1541894\n")
    
    # 运行示例
    example_basic_clustering()
    example_find_optimal_clusters()
    example_analyze_csv_file()
    example_customer_segmentation()
    
    print("\n" + "=" * 60)
    print("安装依赖:")
    print("  pip install pandas scikit-learn numpy")
    print("=" * 60)
