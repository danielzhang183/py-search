#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web爬虫模块

提供通用的爬虫功能，包括：
1. HTTP请求（支持重试、代理）
2. HTML解析
3. 数据保存
4. 反爬虫处理
"""

import os
import time
import random
import csv
import json
import pickle
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin, urlparse, urlunparse
import re

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    _has_requests = True
except ImportError:
    _has_requests = False

try:
    from bs4 import BeautifulSoup
    _has_bs4 = True
    _BeautifulSoup = BeautifulSoup  # 保存引用用于类型注解
except ImportError:
    _has_bs4 = False
    _BeautifulSoup = None  # 占位符

try:
    from fake_useragent import UserAgent
    _has_fake_ua = True
except ImportError:
    _has_fake_ua = False


class WebScraper:
    """Web爬虫类"""
    
    def __init__(self, headers: Optional[Dict] = None, use_random_ua: bool = True):
        """
        初始化爬虫
        
        Args:
            headers: 自定义请求头
            use_random_ua: 是否使用随机User-Agent
        """
        if not _has_requests:
            raise ImportError("requests未安装，请运行: pip install requests")
        
        self.session = requests.Session()
        
        # 设置请求头
        if use_random_ua and _has_fake_ua:
            try:
                ua = UserAgent()
                default_headers = {'User-Agent': ua.random}
            except:
                default_headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
        else:
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """
        发送GET请求
        
        Args:
            url: 目标URL
            **kwargs: 其他requests参数
            
        Returns:
            Response对象或None
        """
        try:
            response = self.session.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"GET请求失败 {url}: {e}")
            return None
    
    def post(self, url: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> Optional[requests.Response]:
        """
        发送POST请求
        
        Args:
            url: 目标URL
            data: 表单数据
            json: JSON数据
            **kwargs: 其他requests参数
            
        Returns:
            Response对象或None
        """
        try:
            response = self.session.post(url, data=data, json=json, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"POST请求失败 {url}: {e}")
            return None
    
    def parse_html(self, html_content: str, parser: str = 'lxml'):
        """
        解析HTML内容
        
        Args:
            html_content: HTML字符串
            parser: 解析器类型（'lxml', 'html.parser', 'html5lib'）
            
        Returns:
            BeautifulSoup对象或None
        """
        if not _has_bs4:
            raise ImportError("beautifulsoup4未安装，请运行: pip install beautifulsoup4")
        
        try:
            from bs4 import BeautifulSoup
            return BeautifulSoup(html_content, parser)
        except Exception as e:
            print(f"HTML解析失败: {e}")
            return None
    
    def extract_links(self, soup, base_url: Optional[str] = None) -> List[Dict[str, str]]:
        """
        提取所有链接
        
        Args:
            soup: BeautifulSoup对象
            base_url: 基础URL（用于处理相对链接）
            
        Returns:
            链接列表，每个链接包含text和url
        """
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if base_url and not href.startswith('http'):
                href = urljoin(base_url, href)
            links.append({
                'text': a.get_text(strip=True),
                'url': href
            })
        return links
    
    def extract_by_selector(self, soup, selector: str, attr: Optional[str] = None) -> List[str]:
        """
        通过CSS选择器提取内容
        
        Args:
            soup: BeautifulSoup对象
            selector: CSS选择器
            attr: 要提取的属性（None表示提取文本）
            
        Returns:
            提取的内容列表
        """
        elements = soup.select(selector)
        if attr:
            return [elem.get(attr) for elem in elements if elem.get(attr)]
        return [elem.get_text(strip=True) for elem in elements]
    
    def save_cookies(self, filename: str):
        """保存Cookie到文件"""
        with open(filename, 'wb') as f:
            pickle.dump(self.session.cookies, f)
    
    def load_cookies(self, filename: str):
        """从文件加载Cookie"""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
    
    def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """随机延迟"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)


def scrape_and_save(url: str, 
                    output_file: str,
                    selectors: Optional[Dict[str, str]] = None,
                    headers: Optional[Dict] = None) -> bool:
    """
    便捷函数：爬取页面并保存到CSV
    
    Args:
        url: 目标URL
        output_file: 输出CSV文件名
        selectors: CSS选择器字典，格式：{'字段名': 'CSS选择器'}
        headers: 自定义请求头
        
    Returns:
        是否成功
    """
    scraper = WebScraper(headers=headers)
    response = scraper.get(url)
    
    if not response:
        return False
    
    soup = scraper.parse_html(response.text)
    if not soup:
        return False
    
    # 如果没有指定选择器，提取基本信息
    if not selectors:
        data = [{
            'url': url,
            'title': soup.find('title').get_text(strip=True) if soup.find('title') else '',
            'h1': soup.find('h1').get_text(strip=True) if soup.find('h1') else '',
        }]
    else:
        # 根据选择器提取数据
        data = [{}]
        for field, selector in selectors.items():
            values = scraper.extract_by_selector(soup, selector)
            data[0][field] = values[0] if values else ''
    
    # 使用utils模块保存（如果可用）
    try:
        from .utils.file import save_to_csv
        return save_to_csv(data, output_file)
    except ImportError:
        # 回退到直接保存
        if data:
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return True
        return False


# 为了向后兼容，保留这些函数的导入
try:
    from .utils.text import clean_text, extract_numbers, extract_emails
except ImportError:
    # 如果utils模块不存在，提供简单实现
    def clean_text(text: str) -> str:
        """清洗文本：去除多余空白"""
        if not text:
            return ""
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def extract_numbers(text: str) -> List[float]:
        """从文本中提取数字"""
        numbers = re.findall(r'-?\d+\.?\d*', text)
        return [float(n) for n in numbers]
    
    def extract_emails(text: str) -> List[str]:
        """从文本中提取邮箱地址"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
