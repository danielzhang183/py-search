#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试客户数据文件

验证customer_data.csv文件是否创建成功，并显示基本信息
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from py_search import CSVReader
    
    print("=" * 60)
    print("客户数据文件验证")
    print("=" * 60)
    
    # 读取文件
    reader = CSVReader(directory="./examples")
    
    try:
        df = reader.read_with_pandas("customer_data.csv")
        
        print(f"\n✓ 文件读取成功！")
        print(f"\n文件信息:")
        print(f"  - 总行数: {len(df)}")
        print(f"  - 总列数: {len(df.columns)}")
        print(f"  - 列名: {list(df.columns)}")
        
        print(f"\n前5行数据:")
        print(df.head())
        
        print(f"\n数据统计:")
        print(df.describe())
        
        print(f"\n数值列:")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        print(f"  {numeric_cols}")
        
        print(f"\n✓ 文件格式正确，可以进行K-means聚类分析！")
        print(f"\n使用方式:")
        print(f"  from py_search.data_analyzer import kmeans_analyze_csv")
        print(f"  result = kmeans_analyze_csv(")
        print(f"      csv_file='customer_data.csv',")
        print(f"      n_clusters=4,")
        print(f"      directory='./examples'")
        print(f"  )")
        
    except FileNotFoundError:
        print(f"✗ 文件不存在: examples/customer_data.csv")
    except Exception as e:
        print(f"✗ 读取文件时出错: {e}")
        print(f"\n提示: 确保已安装pandas: pip install pandas")
        
except ImportError as e:
    print(f"✗ 导入错误: {e}")
    print(f"\n提示: 确保已安装依赖: pip install pandas")
