# 网页爬取实战路线图

> 从零开始到成功爬取真实网页的完整指南

## 📋 目录

1. [准备工作](#准备工作)
2. [第一步：分析目标网页](#第一步分析目标网页)
3. [第二步：编写基础爬虫](#第二步编写基础爬虫)
4. [第三步：处理反爬虫机制](#第三步处理反爬虫机制)
5. [第四步：数据提取与清洗](#第四步数据提取与清洗)
6. [第五步：数据存储](#第五步数据存储)
7. [第六步：错误处理与重试](#第六步错误处理与重试)
8. [第七步：优化与扩展](#第七步优化与扩展)
9. [实战案例](#实战案例)
10. [常见问题与解决方案](#常见问题与解决方案)

---

## 准备工作

### 1.1 环境配置

```bash
# 安装必要的库
pip3 install requests beautifulsoup4 lxml fake-useragent

# 可选：用于更复杂的场景
pip3 install selenium playwright aiohttp
```

### 1.2 工具准备

- **浏览器开发者工具**：Chrome DevTools / Firefox DevTools
- **HTTP抓包工具**：Charles / Fiddler / Burp Suite（可选）
- **代码编辑器**：VS Code / PyCharm

### 1.3 法律与道德

⚠️ **重要提醒**：

- 遵守网站的 `robots.txt` 规则
- 尊重网站的 `Terms of Service`
- 不要过度频繁请求（添加延迟）
- 不要爬取个人隐私信息
- 遵守相关法律法规（如 GDPR）

---

## 第一步：分析目标网页

### 1.1 打开开发者工具

1. 在浏览器中打开目标网页
2. 按 `F12` 或右键选择"检查"
3. 切换到 `Network` 标签页

### 1.2 分析页面结构

**方法一：静态HTML分析**

```python
# 查看页面源代码
# 右键 -> 查看网页源代码
# 或使用 curl
curl -s "https://example.com" | head -100
```

**方法二：动态内容分析**

- 检查是否有 JavaScript 动态加载
- 查看 Network 标签中的 XHR/Fetch 请求
- 识别 API 端点

### 1.3 识别目标数据

在开发者工具中：

1. **使用选择器工具**（左上角箭头图标）
2. **点击目标元素**，查看 HTML 结构
3. **记录关键信息**：
   - 元素的 CSS 选择器
   - 元素的 class/id 属性
   - 数据所在的标签类型

**示例：分析一个新闻网站**

```html
<!-- 目标：提取新闻标题和链接 -->
<article class="news-item">
    <h2><a href="/news/123">新闻标题</a></h2>
    <p class="summary">新闻摘要...</p>
    <span class="date">2024-01-01</span>
</article>
```

**关键信息记录**：

- 新闻容器：`.news-item` 或 `article.news-item`
- 标题：`h2 a` 或 `.news-item h2 a`
- 链接：`h2 a` 的 `href` 属性
- 摘要：`.summary`
- 日期：`.date`

### 1.4 检查 robots.txt

```bash
# 访问网站的 robots.txt
curl https://example.com/robots.txt
```

**示例 robots.txt**：

```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Crawl-delay: 1
```

---

## 第二步：编写基础爬虫

### 2.1 最简单的爬虫

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础网页爬虫示例
"""
import requests
from bs4 import BeautifulSoup

def simple_scraper(url):
    """最简单的爬虫"""
    # 1. 发送请求
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设置编码
    
    # 2. 解析HTML
    soup = BeautifulSoup(response.text, 'lxml')
    
    # 3. 提取数据
    title = soup.find('title').text
    print(f"页面标题: {title}")
    
    return response.text

# 使用示例
if __name__ == '__main__':
    url = "https://example.com"
    simple_scraper(url)
```

### 2.2 使用项目中的 WebScraper 类

```python
from py_search.web_scraper import WebScraper

# 创建爬虫实例
scraper = WebScraper()

# 发送请求
response = scraper.get("https://example.com")

# 解析HTML
soup = scraper.parse_html(response.text)

# 提取数据
title = soup.find('title').text
print(title)
```

### 2.3 提取多个元素

```python
from py_search.web_scraper import WebScraper
from py_search.utils.text import clean_text

scraper = WebScraper()
response = scraper.get("https://example.com/news")
soup = scraper.parse_html(response.text)

# 提取所有新闻项
news_items = soup.select('.news-item')  # 使用CSS选择器

results = []
for item in news_items:
    title_elem = item.select_one('h2 a')
    summary_elem = item.select_one('.summary')
    date_elem = item.select_one('.date')
    
    if title_elem:
        news = {
            'title': clean_text(title_elem.text),
            'link': title_elem.get('href', ''),
            'summary': clean_text(summary_elem.text) if summary_elem else '',
            'date': clean_text(date_elem.text) if date_elem else ''
        }
        results.append(news)

print(f"提取到 {len(results)} 条新闻")
```

---

## 第三步：处理反爬虫机制

### 3.1 设置请求头

```python
from py_search.web_scraper import WebScraper
from fake_useragent import UserAgent

scraper = WebScraper()

# 方法1：使用随机User-Agent
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

response = scraper.get("https://example.com", headers=headers)
```

### 3.2 添加请求延迟

```python
import time
import random

def scrape_with_delay(url, delay_range=(1, 3)):
    """带延迟的爬取"""
    scraper = WebScraper()
    
    # 随机延迟，模拟人类行为
    delay = random.uniform(*delay_range)
    time.sleep(delay)
    
    response = scraper.get(url)
    return response
```

### 3.3 使用会话（Session）

```python
from py_search.web_scraper import WebScraper

scraper = WebScraper()

# Session会自动保持cookies
response1 = scraper.get("https://example.com/login")
# ... 登录操作 ...
response2 = scraper.get("https://example.com/dashboard")  # 保持登录状态
```

### 3.4 处理 Cookies

```python
# 保存cookies
scraper.save_cookies("cookies.pkl")

# 加载cookies
scraper.load_cookies("cookies.pkl")
```

### 3.5 处理 JavaScript 渲染的页面

如果页面内容由 JavaScript 动态加载，需要使用 Selenium 或 Playwright：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_js_page(url):
    """爬取JavaScript渲染的页面"""
    driver = webdriver.Chrome()  # 或 Firefox()
    
    try:
        driver.get(url)
        
        # 等待元素加载
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content"))
        )
        
        # 获取页面源码
        html = driver.page_source
        
        # 使用BeautifulSoup解析
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        
        return soup
    finally:
        driver.quit()
```

---

## 第四步：数据提取与清洗

### 4.1 使用 CSS 选择器

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'lxml')

# 常用选择器
titles = soup.select('h2.title')           # 类选择器
links = soup.select('a[href]')            # 属性选择器
items = soup.select('div.container > ul > li')  # 子选择器
first = soup.select_one('.first-item')    # 只选第一个
```

### 4.2 使用文本工具函数清洗数据

```python
from py_search.utils.text import clean_text, remove_html_tags, extract_numbers, extract_emails

# 清洗文本
dirty_text = "  这是  一段\n\n有问题的文本  "
clean = clean_text(dirty_text)  # "这是 一段 有问题的文本"

# 移除HTML标签
html_text = "<p>这是<strong>文本</strong></p>"
plain = remove_html_tags(html_text)  # "这是 文本"

# 提取数字
text = "价格：¥99.99，数量：10"
numbers = extract_numbers(text)  # [99.99, 10.0]

# 提取邮箱
text = "联系邮箱：contact@example.com"
emails = extract_emails(text)  # ['contact@example.com']
```

### 4.3 处理相对链接

```python
from py_search.utils.text import normalize_url

base_url = "https://example.com"
relative_link = "/news/123"
absolute_link = normalize_url(relative_link, base_url)
# 结果: "https://example.com/news/123"
```

### 4.4 数据验证

```python
def validate_news_item(item):
    """验证新闻数据"""
    required_fields = ['title', 'link']
    
    for field in required_fields:
        if not item.get(field):
            return False
    
    # 验证链接格式
    link = item['link']
    if not link.startswith(('http://', 'https://', '/')):
        return False
    
    return True

# 使用
valid_items = [item for item in news_items if validate_news_item(item)]
```

---

## 第五步：数据存储

### 5.1 保存为 CSV

```python
from py_search.utils.file import save_to_csv

data = [
    {'title': '新闻1', 'link': 'https://example.com/1', 'date': '2024-01-01'},
    {'title': '新闻2', 'link': 'https://example.com/2', 'date': '2024-01-02'},
]

save_to_csv(data, 'news.csv')
```

### 5.2 保存为 JSON

```python
from py_search.utils.file import save_to_json

data = {
    'total': 100,
    'items': [
        {'title': '新闻1', 'link': 'https://example.com/1'},
        {'title': '新闻2', 'link': 'https://example.com/2'},
    ]
}

save_to_json(data, 'news.json')
```

### 5.3 保存为 Excel

```python
from py_search.utils.file import save_to_excel

data = [
    {'title': '新闻1', 'link': 'https://example.com/1'},
    {'title': '新闻2', 'link': 'https://example.com/2'},
]

save_to_excel(data, 'news.xlsx', sheet_name='新闻列表')
```

### 5.4 使用便捷函数

```python
from py_search.web_scraper import scrape_and_save

# 爬取并直接保存
scrape_and_save(
    url="https://example.com/news",
    output_file="news.csv",
    selectors={
        'title': 'h2.title',
        'link': 'h2.title a',
        'summary': '.summary'
    }
)
```

---

## 第六步：错误处理与重试

### 6.1 基础错误处理

```python
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

def safe_scrape(url, max_retries=3):
    """带错误处理的爬取"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查HTTP状态码
            return response
        except Timeout:
            print(f"请求超时，重试 {attempt + 1}/{max_retries}")
            if attempt == max_retries - 1:
                raise
        except ConnectionError:
            print(f"连接错误，重试 {attempt + 1}/{max_retries}")
            if attempt == max_retries - 1:
                raise
        except RequestException as e:
            print(f"请求失败: {e}")
            raise
        except Exception as e:
            print(f"未知错误: {e}")
            raise
    
    return None
```

### 6.2 使用指数退避重试

```python
import time
import random

def scrape_with_backoff(url, max_retries=5):
    """指数退避重试"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            # 指数退避：1s, 2s, 4s, 8s...
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"等待 {wait_time:.2f} 秒后重试...")
            time.sleep(wait_time)
    
    return None
```

### 6.3 处理HTTP状态码

```python
def handle_status_code(response):
    """处理不同的HTTP状态码"""
    status = response.status_code
    
    if status == 200:
        return response
    elif status == 403:
        raise Exception("访问被禁止，可能需要登录或更换User-Agent")
    elif status == 404:
        raise Exception("页面不存在")
    elif status == 429:
        raise Exception("请求过于频繁，需要降低请求速度")
    elif status == 500:
        raise Exception("服务器错误")
    else:
        response.raise_for_status()
    
    return response
```

### 6.4 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def scrape_with_logging(url):
    """带日志的爬取"""
    logger.info(f"开始爬取: {url}")
    
    try:
        response = requests.get(url)
        logger.info(f"成功获取页面，状态码: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"爬取失败: {e}", exc_info=True)
        raise
```

---

## 第七步：优化与扩展

### 7.1 多页面爬取

```python
from py_search.web_scraper import WebScraper
from py_search.utils.text import normalize_url
import time

def scrape_multiple_pages(base_url, max_pages=10):
    """爬取多个页面"""
    scraper = WebScraper()
    all_data = []
    
    for page in range(1, max_pages + 1):
        # 构建URL（根据实际网站调整）
        url = f"{base_url}?page={page}"
        
        try:
            response = scraper.get(url)
            soup = scraper.parse_html(response.text)
            
            # 提取数据
            items = extract_items(soup)
            all_data.extend(items)
            
            print(f"已爬取第 {page} 页，获取 {len(items)} 条数据")
            
            # 延迟
            time.sleep(2)
        except Exception as e:
            print(f"第 {page} 页爬取失败: {e}")
            break
    
    return all_data
```

### 7.2 异步爬取（提高效率）

```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_page(session, url):
    """异步获取页面"""
    async with session.get(url) as response:
        return await response.text()

async def scrape_multiple_async(urls):
    """异步爬取多个URL"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        htmls = await asyncio.gather(*tasks)
    
    results = []
    for html in htmls:
        soup = BeautifulSoup(html, 'lxml')
        items = extract_items(soup)
        results.extend(items)
    
    return results

# 使用
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]
results = asyncio.run(scrape_multiple_async(urls))
```

### 7.3 使用代理

```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080',
}

response = requests.get(url, proxies=proxies)
```

### 7.4 数据去重

```python
def remove_duplicates(items, key='link'):
    """根据指定字段去重"""
    seen = set()
    unique_items = []
    
    for item in items:
        value = item.get(key)
        if value and value not in seen:
            seen.add(value)
            unique_items.append(item)
    
    return unique_items

# 使用
unique_news = remove_duplicates(news_items, key='link')
```

---

## 实战案例

### 案例1：爬取新闻网站标题和链接

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实战案例：爬取新闻网站
"""
from py_search.web_scraper import WebScraper
from py_search.utils.text import clean_text, normalize_url
from py_search.utils.file import save_to_csv
import time

def scrape_news_site(base_url):
    """爬取新闻网站"""
    scraper = WebScraper()
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = scraper.get(base_url, headers=headers)
    soup = scraper.parse_html(response.text)
    
    # 提取新闻项
    news_items = soup.select('article.news-item')
    
    results = []
    for item in news_items:
        title_elem = item.select_one('h2 a')
        if not title_elem:
            continue
        
        title = clean_text(title_elem.text)
        link = title_elem.get('href', '')
        
        # 处理相对链接
        if link and not link.startswith('http'):
            link = normalize_url(link, base_url)
        
        summary_elem = item.select_one('.summary')
        summary = clean_text(summary_elem.text) if summary_elem else ''
        
        date_elem = item.select_one('.date')
        date = clean_text(date_elem.text) if date_elem else ''
        
        results.append({
            'title': title,
            'link': link,
            'summary': summary,
            'date': date
        })
    
    return results

# 使用
if __name__ == '__main__':
    url = "https://example.com/news"
    news = scrape_news_site(url)
    
    print(f"爬取到 {len(news)} 条新闻")
    
    # 保存数据
    save_to_csv(news, 'news.csv')
    print("数据已保存到 news.csv")
```

### 案例2：爬取商品信息（带分页）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实战案例：爬取商品信息（多页）
"""
from py_search.web_scraper import WebScraper
from py_search.utils.text import clean_text, extract_numbers
from py_search.utils.file import save_to_csv
import time
import random

def scrape_products(base_url, max_pages=5):
    """爬取商品信息"""
    scraper = WebScraper()
    all_products = []
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        
        try:
            response = scraper.get(url)
            soup = scraper.parse_html(response.text)
            
            # 提取商品
            products = soup.select('.product-item')
            
            for product in products:
                name_elem = product.select_one('.product-name')
                price_elem = product.select_one('.price')
                image_elem = product.select_one('img')
                
                if not name_elem:
                    continue
                
                name = clean_text(name_elem.text)
                price_text = clean_text(price_elem.text) if price_elem else ''
                prices = extract_numbers(price_text)
                price = prices[0] if prices else 0
                
                image_url = image_elem.get('src', '') if image_elem else ''
                
                all_products.append({
                    'name': name,
                    'price': price,
                    'image_url': image_url
                })
            
            print(f"第 {page} 页：获取 {len(products)} 个商品")
            
            # 随机延迟
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"第 {page} 页失败: {e}")
            break
    
    return all_products

# 使用
if __name__ == '__main__':
    url = "https://example.com/products"
    products = scrape_products(url, max_pages=10)
    
    save_to_csv(products, 'products.csv')
    print(f"共爬取 {len(products)} 个商品，已保存到 products.csv")
```

### 案例3：爬取需要登录的网站

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实战案例：爬取需要登录的网站
"""
from py_search.web_scraper import WebScraper
from py_search.utils.file import save_to_csv
import time

def login_and_scrape(login_url, username, password, target_url):
    """登录并爬取"""
    scraper = WebScraper()
    
    # 1. 访问登录页面
    login_page = scraper.get(login_url)
    
    # 2. 提交登录表单
    login_data = {
        'username': username,
        'password': password,
    }
    
    response = scraper.post(login_url, data=login_data)
    
    # 3. 检查登录是否成功
    if 'dashboard' in response.url or 'welcome' in response.text.lower():
        print("登录成功")
    else:
        print("登录失败")
        return []
    
    # 4. 保存cookies（可选）
    scraper.save_cookies('cookies.pkl')
    
    # 5. 访问目标页面
    time.sleep(1)  # 等待一下
    target_response = scraper.get(target_url)
    soup = scraper.parse_html(target_response.text)
    
    # 6. 提取数据
    items = soup.select('.data-item')
    results = []
    
    for item in items:
        # 提取逻辑...
        pass
    
    return results

# 使用
if __name__ == '__main__':
    login_url = "https://example.com/login"
    target_url = "https://example.com/data"
    
    results = login_and_scrape(
        login_url=login_url,
        username="your_username",
        password="your_password",
        target_url=target_url
    )
    
    save_to_csv(results, 'data.csv')
```

---

## 常见问题与解决方案

### Q1: 返回 403 Forbidden

**原因**：网站检测到爬虫行为

**解决方案**：

1. 更换 User-Agent
2. 添加更多请求头（Referer, Accept等）
3. 使用代理
4. 增加请求延迟
5. 使用 Selenium 模拟真实浏览器

### Q2: 页面内容为空或乱码

**原因**：编码问题或JavaScript渲染

**解决方案**：

```python
# 设置正确的编码
response.encoding = 'utf-8'

# 或使用chardet自动检测
import chardet
encoding = chardet.detect(response.content)['encoding']
response.encoding = encoding

# 如果是JavaScript渲染，使用Selenium
```

### Q3: 连接超时

**原因**：网络问题或服务器响应慢

**解决方案**：

```python
# 增加超时时间
response = requests.get(url, timeout=30)

# 使用重试机制
# 参考第六步的错误处理
```

### Q4: 数据提取不准确

**原因**：选择器不正确或页面结构变化

**解决方案**：

1. 使用浏览器开发者工具验证选择器
2. 使用更通用的选择器
3. 添加数据验证
4. 定期检查页面结构

### Q5: 爬取速度太慢

**原因**：同步请求，单线程

**解决方案**：

1. 使用异步请求（aiohttp）
2. 使用多线程/多进程
3. 减少不必要的延迟
4. 批量处理数据

### Q6: 被封IP

**原因**：请求过于频繁

**解决方案**：

1. 大幅增加延迟时间
2. 使用代理池
3. 降低并发数
4. 遵守 robots.txt 的 crawl-delay

---

## 完整示例：端到端爬虫

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的网页爬虫示例
包含：错误处理、重试、数据清洗、保存
"""
from py_search.web_scraper import WebScraper
from py_search.utils.text import clean_text, normalize_url
from py_search.utils.file import save_to_csv, save_to_json
import time
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteScraper:
    """完整的爬虫类"""
    
    def __init__(self, base_url, delay_range=(1, 3)):
        self.scraper = WebScraper()
        self.base_url = base_url
        self.delay_range = delay_range
        self.all_data = []
    
    def scrape_page(self, url, max_retries=3):
        """爬取单个页面（带重试）"""
        for attempt in range(max_retries):
            try:
                time.sleep(random.uniform(*self.delay_range))
                
                response = self.scraper.get(url)
                response.raise_for_status()
                
                return self.scraper.parse_html(response.text)
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次尝试失败: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # 指数退避
        
        return None
    
    def extract_data(self, soup):
        """提取数据（根据实际网站调整）"""
        items = soup.select('.target-item')
        results = []
        
        for item in items:
            try:
                data = {
                    'title': clean_text(item.select_one('.title').text),
                    'link': normalize_url(
                        item.select_one('a').get('href', ''),
                        self.base_url
                    ),
                    'description': clean_text(
                        item.select_one('.desc').text
                    ) if item.select_one('.desc') else '',
                }
                results.append(data)
            except Exception as e:
                logger.warning(f"提取数据失败: {e}")
                continue
        
        return results
    
    def scrape_all(self, max_pages=10):
        """爬取所有页面"""
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}?page={page}"
            
            try:
                logger.info(f"爬取第 {page} 页: {url}")
                soup = self.scrape_page(url)
                
                if soup:
                    data = self.extract_data(soup)
                    self.all_data.extend(data)
                    logger.info(f"第 {page} 页：获取 {len(data)} 条数据")
                else:
                    logger.warning(f"第 {page} 页：未获取到数据")
                    break
                    
            except Exception as e:
                logger.error(f"第 {page} 页失败: {e}")
                break
        
        return self.all_data
    
    def save(self, filename, format='csv'):
        """保存数据"""
        if format == 'csv':
            save_to_csv(self.all_data, filename)
        elif format == 'json':
            save_to_json(self.all_data, filename)
        else:
            raise ValueError(f"不支持的格式: {format}")
        
        logger.info(f"数据已保存到 {filename}")

# 使用示例
if __name__ == '__main__':
    scraper = CompleteScraper(
        base_url="https://example.com/news",
        delay_range=(1, 3)
    )
    
    data = scraper.scrape_all(max_pages=5)
    print(f"共爬取 {len(data)} 条数据")
    
    scraper.save('results.csv', format='csv')
    scraper.save('results.json', format='json')
```

---

## 总结

### 爬虫开发流程检查清单

- [ ] 分析目标网页结构
- [ ] 检查 robots.txt
- [ ] 编写基础爬虫
- [ ] 添加请求头和延迟
- [ ] 实现错误处理和重试
- [ ] 数据提取和清洗
- [ ] 数据验证
- [ ] 数据存储
- [ ] 测试和调试
- [ ] 优化性能
- [ ] 遵守法律法规

### 最佳实践

1. **始终添加延迟**：避免对服务器造成压力
2. **使用随机User-Agent**：降低被检测风险
3. **实现错误处理**：提高爬虫稳定性
4. **保存中间结果**：防止数据丢失
5. **记录日志**：便于调试和监控
6. **遵守规则**：尊重网站和法律法规

### 下一步学习

- 深入学习 Selenium/Playwright（处理JavaScript）
- 学习 Scrapy 框架（大规模爬虫）
- 学习反爬虫技术（验证码、IP封禁等）
- 学习数据清洗和分析
- 学习数据库存储（MySQL, MongoDB等）

---

**祝您爬虫开发顺利！** 🚀
