#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件操作工具函数

提供文件保存、读取等功能
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional

try:
    import pandas as pd
    _has_pandas = True
except ImportError:
    _has_pandas = False


def save_to_csv(data: List[Dict[str, Any]], filename: str, mode: str = 'w') -> bool:
    """
    保存数据到CSV文件
    
    Args:
        data: 数据列表（字典列表）
        filename: 文件名
        mode: 写入模式（'w'覆盖，'a'追加）
        
    Returns:
        是否成功
    """
    if not data:
        return False
    
    try:
        with open(filename, mode, newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            if mode == 'w':
                writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"保存CSV失败: {e}")
        return False


def save_to_json(data: Any, filename: str, indent: int = 2) -> bool:
    """
    保存数据到JSON文件
    
    Args:
        data: 数据（字典或列表）
        filename: 文件名
        indent: JSON缩进
        
    Returns:
        是否成功
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception as e:
        print(f"保存JSON失败: {e}")
        return False


def save_to_excel(data: List[Dict[str, Any]], filename: str, sheet_name: str = 'Sheet1') -> bool:
    """
    保存数据到Excel文件
    
    Args:
        data: 数据列表（字典列表）
        filename: 文件名
        sheet_name: 工作表名称
        
    Returns:
        是否成功
    """
    if not _has_pandas:
        raise ImportError("pandas未安装，请运行: pip install pandas")
    
    if not data:
        return False
    
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, sheet_name=sheet_name, index=False)
        return True
    except Exception as e:
        print(f"保存Excel失败: {e}")
        return False


def ensure_directory(path: str) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
        
    Returns:
        是否成功
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def get_file_size(filename: str) -> Optional[int]:
    """
    获取文件大小（字节）
    
    Args:
        filename: 文件路径
        
    Returns:
        文件大小（字节）或None
    """
    try:
        return os.path.getsize(filename)
    except OSError:
        return None


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的字符串（如 "1.5 MB"）
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
