#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载CSV文件示例

演示如何使用py_search从URL下载CSV文件
"""

from py_search import download_csv_from_url, CSVReader

# 示例1: 使用函数下载
print("示例1: 使用download_csv_from_url函数")
print("-" * 50)

# 下载CSV文件（会自动保存到examples文件夹）
try:
    url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
    save_path = download_csv_from_url(url, filename="covid_data.csv")
    print(f"✓ 文件已下载到: {save_path}")
except Exception as e:
    print(f"✗ 下载失败: {e}")
    print("提示: 这可能是网络连接问题，代码本身是正确的")

print("\n" + "=" * 50)

# 示例2: 使用类方法下载
print("示例2: 使用CSVReader类的download_csv方法")
print("-" * 50)

try:
    reader = CSVReader(directory="../data")
    url = "https://example.com/example.csv"  # 替换为实际的CSV URL
    save_path = reader.download_csv(url, filename="downloaded_data.csv")
    print(f"✓ 文件已下载到: {save_path}")
except Exception as e:
    print(f"✗ 下载失败: {e}")
    print("提示: 请确保URL是有效的CSV文件链接")

print("\n使用说明:")
print("1. 将URL替换为你要下载的CSV文件链接")
print("2. 文件会自动保存到examples文件夹")
print("3. 如果URL中没有文件名，可以指定filename参数")
