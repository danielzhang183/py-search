# Python 爬虫入门指南

## 适合人群

本指南适合有Web开发经验的开发者快速入门Python爬虫。

## 学习资源

### 官方文档和教程

1. **Python官方文档 - urllib**
   - <https://docs.python.org/3/library/urllib.html>
   - Python标准库，无需安装

2. **Requests库官方文档**
   - <https://requests.readthedocs.io/>
   - 最流行的HTTP库，比urllib更易用

3. **Beautiful Soup官方文档**
   - <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
   - HTML/XML解析库

4. **Scrapy官方文档**
   - <https://docs.scrapy.org/>
   - 专业的爬虫框架

5. **Selenium官方文档**
   - <https://www.selenium.dev/documentation/>
   - 浏览器自动化，处理JavaScript渲染的页面

### 推荐学习网站

1. **Real Python - Web Scraping**
   - <https://realpython.com/python-web-scraping-practical-introduction/>
   - 实用性强，适合有经验的开发者

2. **Scrapy官方教程**
   - <https://docs.scrapy.org/en/latest/intro/tutorial.html>
   - 学习专业爬虫框架

3. **Beautiful Soup教程**
   - <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
   - HTML解析入门

4. **Python Web Scraping - GeeksforGeeks**
   - <https://www.geeksforgeeks.org/python-web-scraping-tutorial/>
   - 系统化的教程

### 实战项目

1. **GitHub - Awesome Web Scraping**
   - <https://github.com/lorien/awesome-web-scraping>
   - 爬虫工具和资源集合

2. **Scrapy Examples**
   - <https://github.com/scrapy/scrapy/tree/master/examples>
   - Scrapy官方示例

## 常用库清单

### 核心库（必学）

1. **requests** - HTTP请求库

   ```bash
   pip install requests
   ```

   - 最常用的HTTP库
   - 简单易用，功能强大
   - 支持会话、Cookie、代理等

2. **BeautifulSoup4** - HTML解析库

   ```bash
   pip install beautifulsoup4
   ```

   - 解析HTML/XML
   - 支持多种解析器（lxml, html.parser）
   - 查找元素简单直观

3. **lxml** - 快速XML/HTML解析器

   ```bash
   pip install lxml
   ```

   - BeautifulSoup的推荐解析器
   - 速度快，功能强

### 进阶库

1. **Scrapy** - 爬虫框架

   ```bash
   pip install scrapy
   ```

   - 专业级爬虫框架
   - 适合大规模爬取
   - 内置去重、管道、中间件等

2. **Selenium** - 浏览器自动化

   ```bash
   pip install selenium
   ```

   - 处理JavaScript渲染的页面
   - 模拟真实浏览器操作
   - 需要安装浏览器驱动

3. **Playwright** - 现代浏览器自动化

   ```bash
   pip install playwright
   ```

   - Selenium的现代替代品
   - 支持多浏览器
   - 性能更好

### 辅助库

1. **fake-useragent** - 随机User-Agent

   ```bash
   pip install fake-useragent
   ```

   - 生成随机User-Agent
   - 避免被反爬

2. **urllib3** - HTTP客户端

   ```bash
   pip install urllib3
   ```

   - 底层HTTP库
   - requests基于它构建

3. **httpx** - 异步HTTP客户端

   ```bash
   pip install httpx
   ```

   - 支持异步请求
   - 类似requests的API

4. **pandas** - 数据处理

    ```bash
    pip install pandas
    ```

    - 处理爬取的数据
    - 数据清洗和分析

## 通用函数示例

### 1. 基础HTTP请求

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_page(url, headers=None, timeout=10, retries=3):
    """
    通用GET请求函数
    
    Args:
        url: 目标URL
        headers: 请求头字典
        timeout: 超时时间（秒）
        retries: 重试次数
        
    Returns:
        Response对象或None
    """
    # 默认请求头
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    if headers:
        default_headers.update(headers)
    
    # 配置重试策略
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    try:
        response = session.get(url, headers=default_headers, timeout=timeout)
        response.raise_for_status()  # 检查HTTP错误
        return response
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
response = get_page("https://example.com")
if response:
    print(response.text[:500])
```

### 2. HTML解析

```python
from bs4 import BeautifulSoup
import re

def parse_html(html_content, parser='lxml'):
    """
    解析HTML内容
    
    Args:
        html_content: HTML字符串
        parser: 解析器类型（'lxml', 'html.parser', 'html5lib'）
        
    Returns:
        BeautifulSoup对象
    """
    return BeautifulSoup(html_content, parser)

def extract_links(soup, base_url=None):
    """
    提取所有链接
    
    Args:
        soup: BeautifulSoup对象
        base_url: 基础URL（用于处理相对链接）
        
    Returns:
        链接列表
    """
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if base_url and not href.startswith('http'):
            from urllib.parse import urljoin
            href = urljoin(base_url, href)
        links.append({
            'text': a.get_text(strip=True),
            'url': href
        })
    return links

def extract_text_by_selector(soup, selector, attr=None):
    """
    通过CSS选择器提取文本
    
    Args:
        soup: BeautifulSoup对象
        selector: CSS选择器
        attr: 要提取的属性（None表示提取文本）
        
    Returns:
        提取的内容列表
    """
    elements = soup.select(selector)
    if attr:
        return [elem.get(attr) for elem in elements]
    return [elem.get_text(strip=True) for elem in elements]

# 使用示例
html = """
<html>
<body>
    <h1>标题</h1>
    <a href="/page1">链接1</a>
    <a href="/page2">链接2</a>
</body>
</html>
"""
soup = parse_html(html)
links = extract_links(soup)
print(links)
```

### 3. 数据保存

```python
import csv
import json
import pandas as pd
from datetime import datetime

def save_to_csv(data, filename, mode='w'):
    """
    保存数据到CSV文件
    
    Args:
        data: 数据列表（字典列表）
        filename: 文件名
        mode: 写入模式（'w'覆盖，'a'追加）
    """
    if not data:
        return
    
    with open(filename, mode, newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if mode == 'w':
            writer.writeheader()
        writer.writerows(data)

def save_to_json(data, filename, indent=2):
    """
    保存数据到JSON文件
    
    Args:
        data: 数据（字典或列表）
        filename: 文件名
        indent: JSON缩进
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def save_to_excel(data, filename, sheet_name='Sheet1'):
    """
    保存数据到Excel文件
    
    Args:
        data: 数据列表（字典列表）
        filename: 文件名
        sheet_name: 工作表名称
    """
    if not data:
        return
    
    df = pd.DataFrame(data)
    df.to_excel(filename, sheet_name=sheet_name, index=False)

# 使用示例
data = [
    {'name': '产品1', 'price': 100},
    {'name': '产品2', 'price': 200}
]
save_to_csv(data, 'products.csv')
save_to_json(data, 'products.json')
```

### 4. 反爬虫处理

```python
import time
import random
from fake_useragent import UserAgent

def get_random_headers():
    """
    获取随机User-Agent
    
    Returns:
        包含随机User-Agent的请求头字典
    """
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

def random_delay(min_seconds=1, max_seconds=3):
    """
    随机延迟（避免请求过快）
    
    Args:
        min_seconds: 最小延迟秒数
        max_seconds: 最大延迟秒数
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def use_proxy(url, proxy_dict):
    """
    使用代理发送请求
    
    Args:
        url: 目标URL
        proxy_dict: 代理字典，格式：{'http': 'http://proxy:port', 'https': 'https://proxy:port'}
        
    Returns:
        Response对象
    """
    try:
        response = requests.get(url, proxies=proxy_dict, timeout=10)
        return response
    except Exception as e:
        print(f"代理请求失败: {e}")
        return None

# 使用示例
headers = get_random_headers()
response = get_page("https://example.com", headers=headers)
random_delay(1, 3)  # 延迟1-3秒
```

### 5. 会话管理

```python
class WebScraper:
    """爬虫类，管理会话和Cookie"""
    
    def __init__(self, headers=None):
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        else:
            self.session.headers.update(get_random_headers())
    
    def get(self, url, **kwargs):
        """发送GET请求"""
        try:
            response = self.session.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def post(self, url, data=None, json=None, **kwargs):
        """发送POST请求"""
        try:
            response = self.session.post(url, data=data, json=json, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def save_cookies(self, filename):
        """保存Cookie到文件"""
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.session.cookies, f)
    
    def load_cookies(self, filename):
        """从文件加载Cookie"""
        import pickle
        with open(filename, 'rb') as f:
            self.session.cookies.update(pickle.load(f))

# 使用示例
scraper = WebScraper()
response = scraper.get("https://example.com")
scraper.save_cookies("cookies.pkl")
```

### 6. 异步爬取

```python
import asyncio
import aiohttp
from typing import List

async def fetch_url(session, url):
    """
    异步获取单个URL
    
    Args:
        session: aiohttp会话
        url: 目标URL
        
    Returns:
        (url, html_content) 元组
    """
    try:
        async with session.get(url, timeout=10) as response:
            html = await response.text()
            return (url, html)
    except Exception as e:
        print(f"获取 {url} 失败: {e}")
        return (url, None)

async def fetch_multiple_urls(urls: List[str], max_concurrent=5):
    """
    异步获取多个URL
    
    Args:
        urls: URL列表
        max_concurrent: 最大并发数
        
    Returns:
        [(url, html), ...] 列表
    """
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# 使用示例
# urls = ['https://example.com/page1', 'https://example.com/page2']
# results = asyncio.run(fetch_multiple_urls(urls))
```

### 7. 数据清洗

```python
import re
from typing import Any

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
    # 去除特殊字符（可选）
    # text = re.sub(r'[^\w\s]', '', text)
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

def normalize_url(url: str, base_url: str = None) -> str:
    """
    规范化URL
    
    Args:
        url: 原始URL
        base_url: 基础URL（用于处理相对链接）
        
    Returns:
        规范化后的URL
    """
    from urllib.parse import urljoin, urlparse, urlunparse
    
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

# 使用示例
text = "价格：$99.99，联系邮箱：contact@example.com"
numbers = extract_numbers(text)
emails = extract_emails(text)
print(f"数字: {numbers}, 邮箱: {emails}")
```

## 完整示例：简单爬虫

```python
import requests
from bs4 import BeautifulSoup
import csv
import time
from typing import List, Dict

class SimpleScraper:
    """简单爬虫示例"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_page(self, url: str) -> Dict:
        """
        爬取单个页面
        
        Args:
            url: 目标URL
            
        Returns:
            包含数据的字典
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 提取数据（根据实际网站结构调整）
            data = {
                'url': url,
                'title': soup.find('title').get_text(strip=True) if soup.find('title') else '',
                'h1': soup.find('h1').get_text(strip=True) if soup.find('h1') else '',
                'links': len(soup.find_all('a')),
            }
            
            return data
            
        except Exception as e:
            print(f"爬取 {url} 失败: {e}")
            return None
    
    def scrape_multiple(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """
        爬取多个页面
        
        Args:
            urls: URL列表
            delay: 每次请求之间的延迟（秒）
            
        Returns:
            数据列表
        """
        results = []
        for i, url in enumerate(urls):
            print(f"正在爬取 ({i+1}/{len(urls)}): {url}")
            data = self.scrape_page(url)
            if data:
                results.append(data)
            time.sleep(delay)  # 避免请求过快
        return results

# 使用示例
if __name__ == "__main__":
    scraper = SimpleScraper()
    urls = ['https://example.com', 'https://httpbin.org/html']
    results = scraper.scrape_multiple(urls, delay=1)
    
    # 保存结果
    if results:
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"已保存 {len(results)} 条数据到 scraped_data.csv")
```

## 最佳实践

### 1. 遵守robots.txt

```python
from urllib.robotparser import RobotFileParser

def can_fetch(url, user_agent='*'):
    """检查是否可以爬取该URL"""
    rp = RobotFileParser()
    rp.set_url(f"{url}/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)
```

### 2. 错误处理和重试

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_with_retry(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response
```

### 3. 数据验证

```python
def validate_data(data: Dict, required_fields: List[str]) -> bool:
    """验证数据完整性"""
    return all(field in data and data[field] for field in required_fields)
```

## 注意事项

1. **遵守法律法规**：不要爬取受版权保护的内容
2. **尊重网站**：控制请求频率，避免对服务器造成压力
3. **检查robots.txt**：遵守网站的爬虫协议
4. **处理异常**：网络请求可能失败，要有完善的错误处理
5. **数据存储**：及时保存数据，避免重复爬取
6. **反爬虫**：了解常见的反爬虫机制（验证码、IP封禁等）

## 进阶学习

1. **Scrapy框架**：学习专业的爬虫框架
2. **Selenium/Playwright**：处理JavaScript渲染的页面
3. **分布式爬虫**：使用Scrapy-Redis等实现分布式
4. **数据存储**：学习MongoDB、MySQL等数据库存储
5. **反爬虫对抗**：学习验证码识别、IP代理池等

## 推荐工具

- **Postman/Insomnia**：测试API请求
- **浏览器开发者工具**：分析网页结构
- **XPath Helper**：Chrome扩展，测试XPath
- **SelectorGadget**：Chrome扩展，快速生成CSS选择器
