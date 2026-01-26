#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV文件读取模块

提供两种方式读取CSV文件：
1. 使用标准库（csv模块）
2. 使用pandas库（功能更强大）
"""

import os
import glob
import csv
from typing import List, Optional, Dict, Any


class CSVReader:
    """CSV文件读取器类"""
    
    def __init__(self, directory: Optional[str] = None, encoding: str = 'utf-8'):
        """
        初始化CSV读取器
        
        Args:
            directory: 要读取的目录路径，如果为None则使用当前目录
            encoding: 文件编码，默认为utf-8
        """
        self.directory = directory or os.getcwd()
        self.encoding = encoding
    
    def find_csv_files(self) -> List[str]:
        """
        查找目录下的所有CSV文件
        
        Returns:
            CSV文件路径列表
        """
        csv_files = glob.glob(os.path.join(self.directory, "*.csv"))
        return csv_files
    
    def read_with_standard_lib(self, csv_file: str) -> List[List[str]]:
        """
        使用标准库读取CSV文件
        
        Args:
            csv_file: CSV文件路径（可以是完整路径或相对路径）
            
        Returns:
            包含所有行的列表
        """
        rows = []
        # 如果是绝对路径或已存在的完整路径，直接使用；否则拼接目录
        if os.path.isabs(csv_file) or os.path.exists(csv_file):
            csv_path = csv_file
        else:
            csv_path = os.path.join(self.directory, csv_file)
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"文件不存在: {csv_path}")
        
        with open(csv_path, 'r', encoding=self.encoding) as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        
        return rows
    
    def read_with_pandas(self, csv_file: str):
        """
        使用pandas读取CSV文件
        
        Args:
            csv_file: CSV文件路径（可以是完整路径或相对路径）
            
        Returns:
            pandas DataFrame对象
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas未安装，请运行: pip install pandas")
        
        # 如果是绝对路径或已存在的完整路径，直接使用；否则拼接目录
        if os.path.isabs(csv_file) or os.path.exists(csv_file):
            csv_path = csv_file
        else:
            csv_path = os.path.join(self.directory, csv_file)
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"文件不存在: {csv_path}")
        
        return pd.read_csv(csv_path, encoding=self.encoding)
    
    def get_file_info(self, csv_file: str) -> Dict[str, Any]:
        """
        获取CSV文件的基本信息
        
        Args:
            csv_file: CSV文件路径
            
        Returns:
            包含文件信息的字典
        """
        try:
            df = self.read_with_pandas(csv_file)
            return {
                'filename': os.path.basename(csv_file),
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'dtypes': df.dtypes.to_dict()
            }
        except ImportError:
            # 如果没有pandas，使用标准库获取基本信息
            rows = self.read_with_standard_lib(csv_file)
            return {
                'filename': os.path.basename(csv_file),
                'rows': len(rows),
                'columns': len(rows[0]) if rows else 0,
                'column_names': rows[0] if rows else [],
                'dtypes': None
            }


def read_csv_files(directory: Optional[str] = None, use_pandas: bool = True) -> None:
    """
    读取指定目录下的所有CSV文件并显示信息
    
    Args:
        directory: 要读取的目录路径，如果为None则使用当前目录
        use_pandas: 是否使用pandas读取（需要安装pandas）
    """
    reader = CSVReader(directory)
    csv_files = reader.find_csv_files()
    
    if not csv_files:
        print("当前文件夹下没有找到CSV文件")
        return
    
    for csv_file in csv_files:
        print(f"\n正在读取: {os.path.basename(csv_file)}")
        print("-" * 50)
        
        try:
            if use_pandas:
                df = reader.read_with_pandas(csv_file)
                print(f"行数: {len(df)}")
                print(f"列数: {len(df.columns)}")
                print(f"列名: {list(df.columns)}")
                print("\n前5行数据:")
                print(df.head())
                print("\n数据类型:")
                print(df.dtypes)
            else:
                rows = reader.read_with_standard_lib(csv_file)
                print(f"行数: {len(rows)}")
                if rows:
                    print(f"列数: {len(rows[0])}")
                    print(f"列名: {rows[0]}")
                    print("\n前5行数据:")
                    for i, row in enumerate(rows[:5]):
                        print(f"第{i+1}行: {row}")
        except Exception as e:
            print(f"读取文件时出错: {e}")


def read_csv_simple(csv_filename: str, directory: Optional[str] = None) -> None:
    """
    读取指定的CSV文件（简单版本，使用标准库）
    
    Args:
        csv_filename: CSV文件名
        directory: 文件所在目录，如果为None则使用当前目录
    """
    reader = CSVReader(directory)
    
    try:
        rows = reader.read_with_standard_lib(csv_filename)
        print(f"\n读取文件: {csv_filename}")
        print("-" * 40)
        for i, row in enumerate(rows[:5]):  # 只显示前5行
            print(f"第{i+1}行: {row}")
        if len(rows) > 5:
            print("...")
    except Exception as e:
        print(f"读取文件时出错: {e}")
