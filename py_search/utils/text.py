#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本处理工具函数

提供文本清洗、提取、格式化等功能
"""

import re
from typing import List, Optional
from urllib.parse import urljoin, urlparse, urlunparse


def clean_text(text: str) -> str:
    """
    清洗文本：去除多余空白、换行等
    
    Args:
        text: 原始文本
        
    Returns:
        清洗后的文本
    """
    if not text:
        return ""
    # 去除首尾空白
    text = text.strip()
    # 合并多个空白字符
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_numbers(text: str) -> List[float]:
    """
    从文本中提取数字
    
    Args:
        text: 文本内容
        
    Returns:
        数字列表
    """
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return [float(n) for n in numbers]


def extract_emails(text: str) -> List[str]:
    """
    从文本中提取邮箱地址
    
    Args:
        text: 文本内容
        
    Returns:
        邮箱地址列表
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)


def normalize_url(url: str, base_url: Optional[str] = None) -> str:
    """
    规范化URL
    
    Args:
        url: 原始URL
        base_url: 基础URL（用于处理相对链接）
        
    Returns:
        规范化后的URL
    """
    if base_url:
        url = urljoin(base_url, url)
    
    parsed = urlparse(url)
    # 移除fragment
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        ''  # fragment设为空
    ))
    return normalized


def remove_html_tags(text: str) -> str:
    """
    移除HTML标签
    
    Args:
        text: 包含HTML标签的文本
        
    Returns:
        纯文本
    """
    clean = re.sub(r'<[^>]+>', '', text)
    return clean_text(clean)


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    截断文本到指定长度
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后的后缀
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
