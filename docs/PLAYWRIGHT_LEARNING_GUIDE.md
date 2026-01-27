# Playwright 爬虫深入学习指南

> 从入门到精通 Playwright 在爬虫中的实际应用

## 📋 目录

1. [为什么选择 Playwright](#为什么选择-playwright)
2. [Playwright vs 其他工具](#playwright-vs-其他工具)
3. [在爬虫中的实际效用](#在爬虫中的实际效用)
4. [快速开始](#快速开始)
5. [核心 API 详解](#核心-api-详解)
6. [实战案例](#实战案例)
7. [高级技巧](#高级技巧)
8. [性能优化](#性能优化)
9. [反爬虫对抗](#反爬虫对抗)
10. [最佳实践](#最佳实践)
11. [学习资源](#学习资源)

---

## 为什么选择 Playwright

### Playwright 的优势

1. **多浏览器支持**
   - Chromium（Chrome/Edge）
   - Firefox
   - WebKit（Safari）
   - 统一 API，跨浏览器一致

2. **性能卓越**
   - 比 Selenium 快 2-3 倍
   - 原生异步支持
   - 自动等待机制，减少不必要的等待

3. **强大的功能**
   - 自动等待元素
   - 网络拦截和修改
   - 截图和视频录制
   - 地理位置模拟
   - 设备模拟

4. **现代化设计**
   - 原生支持 async/await
   - 更好的错误信息
   - 自动生成代码（Codegen）
   - 强大的调试工具

5. **反检测能力强**
   - 更接近真实浏览器
   - 可以隐藏自动化特征
   - 支持 CDP（Chrome DevTools Protocol）

---

## Playwright vs 其他工具

### Playwright vs Selenium

| 特性 | Playwright | Selenium |
| ------ | ----------- | ---------- |
| **速度** | ⭐⭐⭐⭐⭐ 快 | ⭐⭐⭐ 较慢 |
| **API设计** | ⭐⭐⭐⭐⭐ 现代化 | ⭐⭐⭐ 传统 |
| **自动等待** | ⭐⭐⭐⭐⭐ 内置 | ⭐⭐ 需手动 |
| **多浏览器** | ⭐⭐⭐⭐⭐ 统一API | ⭐⭐⭐ 需不同驱动 |
| **网络拦截** | ⭐⭐⭐⭐⭐ 强大 | ⭐⭐ 有限 |
| **学习曲线** | ⭐⭐⭐⭐ 中等 | ⭐⭐⭐ 中等 |
| **社区** | ⭐⭐⭐⭐ 增长中 | ⭐⭐⭐⭐⭐ 成熟 |
| **文档** | ⭐⭐⭐⭐⭐ 优秀 | ⭐⭐⭐⭐ 良好 |

### Playwright vs Puppeteer

| 特性 | Playwright | Puppeteer |
| ------ | ----------- | ----------- |
| **浏览器支持** | Chromium, Firefox, WebKit | 仅 Chromium |
| **API设计** | 更统一 | Chrome 特定 |
| **跨平台** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **维护** | Microsoft 维护 | Google 维护 |

### 适用场景对比

**使用 Playwright 的场景：**

- ✅ 需要处理 JavaScript 渲染的页面
- ✅ 需要模拟真实用户行为
- ✅ 需要跨浏览器测试
- ✅ 需要网络拦截和修改
- ✅ 需要高性能爬虫
- ✅ 需要反检测能力

**使用 requests + BeautifulSoup 的场景：**

- ✅ 静态 HTML 页面
- ✅ 简单的 API 调用
- ✅ 不需要 JavaScript 渲染
- ✅ 追求最高性能

**使用 Selenium 的场景：**

- ✅ 已有 Selenium 代码库
- ✅ 需要特定浏览器驱动
- ✅ 团队熟悉 Selenium

---

## 在爬虫中的实际效用

### 1. 处理 JavaScript 渲染的页面

**问题**：很多现代网站使用 React、Vue 等框架，内容由 JavaScript 动态加载。

**解决方案**：Playwright 可以等待 JavaScript 执行完成后再提取数据。

```python
from playwright.sync_api import sync_playwright

def scrape_spa_page(url):
    """爬取单页应用（SPA）"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 访问页面，自动等待 JavaScript 执行
        page.goto(url, wait_until='networkidle')
        
        # 等待特定元素出现
        page.wait_for_selector('.content')
        
        # 提取数据
        title = page.locator('h1').inner_text()
        items = page.locator('.item').all()
        
        data = []
        for item in items:
            data.append({
                'text': item.inner_text(),
                'link': item.get_attribute('href')
            })
        
        browser.close()
        return data
```

### 2. 处理动态加载内容

**问题**：页面内容通过 AJAX 或滚动加载。

**解决方案**：Playwright 可以模拟滚动、点击等操作。

```python
def scrape_infinite_scroll(url):
    """爬取无限滚动页面"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # 滚动到底部，加载更多内容
        previous_height = 0
        while True:
            # 滚动到底部
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            
            # 等待新内容加载
            page.wait_for_timeout(2000)
            
            # 检查是否还有新内容
            current_height = page.evaluate('document.body.scrollHeight')
            if current_height == previous_height:
                break
            previous_height = current_height
        
        # 提取所有内容
        items = page.locator('.item').all()
        return [item.inner_text() for item in items]
```

### 3. 处理登录和认证

**问题**：需要登录才能访问的页面。

**解决方案**：Playwright 可以保存和复用 cookies。

```python
def login_and_scrape(login_url, username, password, target_url):
    """登录并爬取"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 显示浏览器便于调试
        context = browser.new_context()
        page = context.new_page()
        
        # 访问登录页面
        page.goto(login_url)
        
        # 填写表单
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        
        # 等待登录完成
        page.wait_for_url('**/dashboard**')
        
        # 保存 cookies
        context.storage_state(path='auth.json')
        
        # 访问目标页面
        page.goto(target_url)
        data = page.locator('.data').inner_text()
        
        browser.close()
        return data

# 后续使用保存的 cookies
def scrape_with_saved_auth(url):
    """使用保存的认证信息"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state='auth.json')
        page = context.new_page()
        page.goto(url)
        # ... 爬取数据
```

### 4. 处理反爬虫机制

**问题**：网站检测自动化工具。

**解决方案**：Playwright 可以隐藏自动化特征。

```python
def stealth_scrape(url):
    """隐藏自动化特征"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        
        # 创建上下文，设置更真实的浏览器环境
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
            geolocation={'latitude': 40.7128, 'longitude': -74.0060},
        )
        
        # 注入脚本，隐藏 webdriver 特征
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        page = context.new_page()
        page.goto(url)
        # ... 爬取数据
```

### 5. 网络拦截和修改

**问题**：需要拦截和修改网络请求。

**解决方案**：Playwright 可以拦截请求和响应。

```python
def intercept_requests(url):
    """拦截和修改网络请求"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 拦截请求
        def handle_route(route):
            # 阻止图片加载（提高速度）
            if route.request.resource_type == 'image':
                route.abort()
            else:
                route.continue_()
        
        page.route('**/*', handle_route)
        
        # 拦截响应
        def handle_response(response):
            if '/api/data' in response.url:
                # 修改响应数据
                json_data = response.json()
                # 处理数据...
                print(f"拦截到数据: {json_data}")
        
        page.on('response', handle_response)
        
        page.goto(url)
        # ... 爬取数据
```

### 6. 处理复杂交互

**问题**：需要模拟复杂的用户交互（拖拽、悬停、键盘输入等）。

**解决方案**：Playwright 支持丰富的交互 API。

```python
def complex_interactions(url):
    """复杂交互示例"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # 悬停
        page.hover('.menu-item')
        
        # 拖拽
        page.drag_and_drop('.source', '.target')
        
        # 键盘输入
        page.fill('input', 'Hello World')
        page.keyboard.press('Enter')
        
        # 组合键
        page.keyboard.press('Control+A')
        page.keyboard.press('Control+C')
        
        # 文件上传
        page.set_input_files('input[type="file"]', 'path/to/file.pdf')
        
        # 选择下拉框
        page.select_option('select', 'option-value')
        
        # 多选
        page.select_option('select', ['option1', 'option2'])
```

---

## 快速开始

### 1. 安装

```bash
# 安装 Playwright
pip install playwright

# 安装浏览器（必需）
playwright install chromium
# 或安装所有浏览器
playwright install
```

### 2. 第一个爬虫

```python
from playwright.sync_api import sync_playwright

def simple_scraper(url):
    """最简单的 Playwright 爬虫"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        
        # 创建新页面
        page = browser.new_page()
        
        # 访问 URL
        page.goto(url)
        
        # 提取数据
        title = page.title()
        content = page.locator('body').inner_text()
        
        # 关闭浏览器
        browser.close()
        
        return {'title': title, 'content': content}

# 使用
result = simple_scraper('https://example.com')
print(result)
```

### 3. 异步版本

```python
from playwright.async_api import async_playwright
import asyncio

async def async_scraper(url):
    """异步爬虫"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        title = await page.title()
        content = await page.locator('body').inner_text()
        
        await browser.close()
        return {'title': title, 'content': content}

# 使用
result = asyncio.run(async_scraper('https://example.com'))
```

---

## 核心 API 详解

### 1. 浏览器和页面

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(
        headless=True,           # 无头模式
        slow_mo=1000,            # 慢动作（调试用）
        args=['--start-maximized'] # 启动参数
    )
    
    # 创建浏览器上下文（隔离的会话）
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='...',
        locale='en-US',
    )
    
    # 创建页面
    page = context.new_page()
    
    # 访问 URL
    page.goto(
        'https://example.com',
        wait_until='networkidle',  # 等待网络空闲
        timeout=30000              # 超时时间
    )
```

### 2. 选择器和定位

```python
# CSS 选择器
page.locator('h1')
page.locator('.class-name')
page.locator('#id-name')
page.locator('div > p')  # 子选择器

# XPath
page.locator('xpath=//h1')

# 文本内容
page.locator('text=Hello World')
page.locator('text=/Hello.*/')  # 正则

# 组合选择器
page.locator('div.item').locator('h2')

# 获取所有匹配元素
items = page.locator('.item').all()
for item in items:
    print(item.inner_text())
```

### 3. 等待机制

```python
# 等待元素出现
page.wait_for_selector('.content')

# 等待元素可见
page.wait_for_selector('.content', state='visible')

# 等待元素隐藏
page.wait_for_selector('.loading', state='hidden')

# 等待网络请求
page.wait_for_load_state('networkidle')

# 等待特定 URL
page.wait_for_url('**/dashboard**')

# 等待函数返回 True
page.wait_for_function('document.readyState === "complete"')

# 自定义等待
page.wait_for_timeout(2000)  # 等待 2 秒
```

### 4. 数据提取

```python
# 文本内容
text = page.locator('h1').inner_text()
all_text = page.locator('.item').all_inner_texts()

# HTML 内容
html = page.locator('div').inner_html()

# 属性值
href = page.locator('a').get_attribute('href')
all_hrefs = page.locator('a').get_attribute('href').all()

# 输入框值
value = page.locator('input').input_value()

# 截图
page.screenshot(path='screenshot.png')
element = page.locator('.element')
element.screenshot(path='element.png')

# PDF（仅 Chromium）
page.pdf(path='page.pdf')
```

### 5. 交互操作

```python
# 点击
page.click('button')
page.locator('button').click()

# 双击
page.dblclick('button')

# 填写表单
page.fill('input[name="username"]', 'user123')
page.type('input', 'text', delay=100)  # 模拟打字

# 选择
page.select_option('select', 'value')
page.check('input[type="checkbox"]')
page.uncheck('input[type="checkbox"]')

# 悬停
page.hover('.menu-item')

# 拖拽
page.drag_and_drop('.source', '.target')

# 文件上传
page.set_input_files('input[type="file"]', 'file.pdf')
page.set_input_files('input[type="file"]', ['file1.pdf', 'file2.pdf'])
```

### 6. 网络拦截

```python
# 拦截请求
def handle_route(route):
    if route.request.resource_type == 'image':
        route.abort()  # 阻止图片
    else:
        route.continue_()

page.route('**/*', handle_route)

# 修改请求
def modify_request(route):
    route.continue_(
        headers={**route.request.headers, 'X-Custom': 'value'}
    )

page.route('**/api/**', modify_request)

# 模拟响应
def mock_response(route):
    route.fulfill(
        status=200,
        body='{"data": "mocked"}',
        headers={'Content-Type': 'application/json'}
    )

page.route('**/api/data', mock_response)
```

### 7. JavaScript 执行

```python
# 执行 JavaScript
result = page.evaluate('document.title')

# 传递参数
result = page.evaluate('(arg) => arg.value', {'value': 123})

# 在页面上下文中执行
result = page.evaluate('''() => {
    return {
        title: document.title,
        url: window.location.href
    }
}''')

# 在元素上下文中执行
element = page.locator('.item')
result = element.evaluate('(el) => el.textContent')
```

---

## 实战案例

### 案例1：爬取动态加载的新闻网站

```python
from playwright.sync_api import sync_playwright
import json

def scrape_news_site(base_url):
    """爬取动态加载的新闻网站"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(base_url, wait_until='networkidle')
        
        news_items = []
        
        # 等待新闻列表加载
        page.wait_for_selector('.news-item')
        
        # 提取新闻
        items = page.locator('.news-item').all()
        for item in items:
            title = item.locator('h2').inner_text()
            link = item.locator('a').get_attribute('href')
            summary = item.locator('.summary').inner_text()
            date = item.locator('.date').inner_text()
            
            news_items.append({
                'title': title,
                'link': link,
                'summary': summary,
                'date': date
            })
        
        # 处理分页
        while True:
            next_button = page.locator('a.next')
            if not next_button.is_visible():
                break
            
            next_button.click()
            page.wait_for_load_state('networkidle')
            
            # 提取新页面的新闻
            items = page.locator('.news-item').all()
            for item in items:
                # ... 提取逻辑
                pass
        
        browser.close()
        return news_items
```

### 案例2：爬取需要登录的网站

```python
def scrape_protected_site(login_url, username, password, target_urls):
    """爬取需要登录的网站"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 登录
        page.goto(login_url)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        
        # 等待登录完成
        page.wait_for_url('**/dashboard**')
        
        # 保存认证状态
        context.storage_state(path='auth.json')
        
        all_data = []
        
        # 爬取多个页面
        for url in target_urls:
            page.goto(url)
            page.wait_for_selector('.content')
            
            data = {
                'url': url,
                'title': page.locator('h1').inner_text(),
                'content': page.locator('.content').inner_text()
            }
            all_data.append(data)
        
        browser.close()
        return all_data

# 后续使用保存的认证
def scrape_with_auth(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state='auth.json')
        page = context.new_page()
        page.goto(url)
        # ... 爬取数据
```

### 案例3：爬取无限滚动页面

```python
def scrape_infinite_scroll(url, max_scrolls=10):
    """爬取无限滚动页面"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        all_items = []
        scroll_count = 0
        
        while scroll_count < max_scrolls:
            # 提取当前可见的项目
            items = page.locator('.item').all()
            current_count = len(all_items)
            
            for item in items:
                text = item.inner_text()
                if text not in [i['text'] for i in all_items]:
                    all_items.append({
                        'text': text,
                        'link': item.locator('a').get_attribute('href')
                    })
            
            # 如果没有新项目，停止滚动
            if len(all_items) == current_count:
                break
            
            # 滚动到底部
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(2000)  # 等待加载
            scroll_count += 1
        
        browser.close()
        return all_items
```

### 案例4：处理反爬虫网站

```python
def stealth_scrape(url):
    """反检测爬虫"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
            geolocation={'latitude': 40.7128, 'longitude': -74.0060},
            color_scheme='light',
        )
        
        # 隐藏自动化特征
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            window.chrome = {
                runtime: {}
            };
        """)
        
        page = context.new_page()
        
        # 添加随机延迟，模拟人类行为
        import random
        page.goto(url)
        page.wait_for_timeout(random.randint(1000, 3000))
        
        # 随机鼠标移动
        page.mouse.move(
            random.randint(100, 500),
            random.randint(100, 500)
        )
        
        data = page.locator('.content').inner_text()
        
        browser.close()
        return data
```

### 案例5：网络拦截和优化

```python
def optimized_scraper(url):
    """优化的爬虫（拦截资源）"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 拦截不需要的资源
        def handle_route(route):
            # 阻止图片、字体、样式表（如果不需要）
            if route.request.resource_type in ['image', 'font', 'stylesheet']:
                route.abort()
            else:
                route.continue_()
        
        page.route('**/*', handle_route)
        
        # 拦截 API 响应
        def handle_response(response):
            if '/api/data' in response.url:
                # 直接使用 API 数据，而不是解析 HTML
                data = response.json()
                print(f"从 API 获取数据: {data}")
        
        page.on('response', handle_response)
        
        page.goto(url, wait_until='networkidle')
        
        # 提取数据
        content = page.locator('.content').inner_text()
        
        browser.close()
        return content
```

---

## 高级技巧

### 1. 并发爬取

```python
from playwright.async_api import async_playwright
import asyncio

async def scrape_url(page, url):
    """爬取单个 URL"""
    await page.goto(url)
    title = await page.title()
    content = await page.locator('body').inner_text()
    return {'url': url, 'title': title, 'content': content}

async def concurrent_scrape(urls, max_concurrent=5):
    """并发爬取多个 URL"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 创建多个页面
        pages = [await browser.new_page() for _ in range(max_concurrent)]
        
        # 并发爬取
        tasks = []
        for i, url in enumerate(urls):
            page = pages[i % max_concurrent]
            tasks.append(scrape_url(page, url))
        
        results = await asyncio.gather(*tasks)
        
        await browser.close()
        return results

# 使用
urls = ['https://example.com/1', 'https://example.com/2', ...]
results = asyncio.run(concurrent_scrape(urls, max_concurrent=5))
```

### 2. 使用代理

```python
def scrape_with_proxy(url, proxy_server):
    """使用代理爬取"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={
                'server': proxy_server,
                'username': 'user',  # 如果需要认证
                'password': 'pass'
            }
        )
        
        page = browser.new_page()
        page.goto(url)
        # ... 爬取数据
```

### 3. 处理验证码

```python
def handle_captcha(page):
    """处理验证码（需要人工介入或第三方服务）"""
    # 方法1：等待人工解决
    page.wait_for_selector('.captcha-solved', timeout=60000)
    
    # 方法2：使用第三方服务（如 2captcha）
    # captcha_solver = TwoCaptcha(api_key='...')
    # solution = captcha_solver.solve(page)
    
    # 方法3：截图并提示用户
    page.screenshot(path='captcha.png')
    print("请查看 captcha.png 并手动解决验证码")
    input("按 Enter 继续...")
```

### 4. 设备模拟

```python
def scrape_mobile(url):
    """模拟移动设备"""
    with sync_playwright() as p:
        # 使用移动设备配置
        iphone = p.devices['iPhone 12']
        
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**iphone)
        page = context.new_page()
        
        page.goto(url)
        # ... 爬取数据
```

### 5. 视频录制

```python
def record_scraping(url, output_video='scraping.mp4'):
    """录制爬取过程"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir='./videos')
        page = context.new_page()
        
        page.goto(url)
        # ... 执行操作
        
        context.close()
        # 视频会自动保存
```

---

## 性能优化

### 1. 资源拦截

```python
# 阻止不需要的资源加载
def handle_route(route):
    if route.request.resource_type in ['image', 'font', 'media']:
        route.abort()
    else:
        route.continue_()

page.route('**/*', handle_route)
```

### 2. 并发控制

```python
# 使用异步 API 并发爬取
async def async_scrape(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        tasks = []
        for url in urls:
            page = await browser.new_page()
            tasks.append(scrape_page(page, url))
        results = await asyncio.gather(*tasks)
        await browser.close()
        return results
```

### 3. 复用浏览器上下文

```python
# 复用上下文，避免重复启动浏览器
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    
    for url in urls:
        page = context.new_page()
        page.goto(url)
        # ... 爬取
        page.close()  # 只关闭页面，不关闭浏览器
```

### 4. 缓存和存储状态

```python
# 保存浏览器状态，避免重复登录
context.storage_state(path='auth.json')

# 后续使用
context = browser.new_context(storage_state='auth.json')
```

---

## 反爬虫对抗

### 1. 隐藏自动化特征

```python
context.add_init_script("""
    // 隐藏 webdriver
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    
    // 伪造 plugins
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });
    
    // 伪造 chrome 对象
    window.chrome = {
        runtime: {}
    };
    
    // 覆盖 permissions
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
    );
""")
```

### 2. 模拟人类行为

```python
import random
import time

def human_like_delay():
    """人类般的延迟"""
    time.sleep(random.uniform(1, 3))

def human_like_typing(page, selector, text):
    """模拟人类打字"""
    page.fill(selector, '')
    for char in text:
        page.type(selector, char, delay=random.randint(50, 150))
        time.sleep(random.uniform(0.05, 0.2))
```

### 3. 使用真实浏览器指纹

```python
context = browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    user_agent='Mozilla/5.0 ...',
    locale='en-US',
    timezone_id='America/New_York',
    permissions=['geolocation'],
    geolocation={'latitude': 40.7128, 'longitude': -74.0060},
    color_scheme='light',
    device_scale_factor=1,
    has_touch=False,
    is_mobile=False,
)
```

---

## 最佳实践

### 1. 错误处理

```python
from playwright.sync_api import TimeoutError

def robust_scrape(url, max_retries=3):
    """健壮的爬虫"""
    for attempt in range(max_retries):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000)
                data = page.locator('.content').inner_text()
                browser.close()
                return data
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
        except Exception as e:
            print(f"错误: {e}")
            raise
```

### 2. 资源管理

```python
# 始终使用 with 语句确保资源释放
with sync_playwright() as p:
    browser = p.chromium.launch()
    try:
        # ... 操作
        pass
    finally:
        browser.close()
```

### 3. 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_scrape(url):
    with sync_playwright() as p:
        logger.info(f"开始爬取: {url}")
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        logger.info("页面加载完成")
        # ... 爬取
        logger.info("爬取完成")
```

### 4. 配置管理

```python
# config.py
PLAYWRIGHT_CONFIG = {
    'headless': True,
    'slow_mo': 0,
    'timeout': 30000,
    'viewport': {'width': 1920, 'height': 1080},
    'user_agent': 'Mozilla/5.0 ...',
}

# 使用
browser = p.chromium.launch(**PLAYWRIGHT_CONFIG)
```

---

## 学习资源

### 官方文档

1. **Playwright 官方文档**
   - 网址：<https://playwright.dev/python/>
   - 推荐度：⭐⭐⭐⭐⭐
   - 内容：最权威、最完整的文档

2. **Playwright API 参考**
   - 网址：<https://playwright.dev/python/docs/api/class-playwright>
   - 推荐度：⭐⭐⭐⭐⭐

3. **Playwright 最佳实践**
   - 网址：<https://playwright.dev/python/docs/best-practices>
   - 推荐度：⭐⭐⭐⭐⭐

### 实战教程

1. **Playwright 官方示例**
   - GitHub：<https://github.com/microsoft/playwright-python>
   - 推荐度：⭐⭐⭐⭐⭐

2. **Real Python - Playwright 教程**
   - 网址：<https://realpython.com/playwright-python/>
   - 推荐度：⭐⭐⭐⭐⭐

### 工具和扩展

1. **Playwright Codegen**（自动生成代码）

   ```bash
   playwright codegen https://example.com
   ```

2. **Playwright Inspector**（调试工具）

   ```bash
   PWDEBUG=1 python script.py
   ```

3. **Playwright Test**（测试框架）

   ```bash
   pip install pytest-playwright
   ```

---

## 总结

### Playwright 在爬虫中的核心价值

1. **处理 JavaScript 渲染**：完美支持现代 SPA 应用
2. **真实浏览器环境**：更接近真实用户，反检测能力强
3. **强大的交互能力**：支持所有用户操作
4. **高性能**：比 Selenium 快 2-3 倍
5. **现代化 API**：原生 async/await 支持

### 适用场景

✅ **适合使用 Playwright：**

- JavaScript 渲染的页面
- 需要登录认证的网站
- 动态加载内容
- 需要复杂交互
- 反爬虫检测严格

❌ **不适合使用 Playwright：**

- 纯静态 HTML 页面（用 requests + BeautifulSoup）
- 简单 API 调用（用 requests）
- 对性能要求极高的场景

### 学习路径

1. **第1周**：安装、基础 API、第一个爬虫
2. **第2周**：选择器、等待机制、数据提取
3. **第3周**：交互操作、网络拦截
4. **第4周**：高级技巧、性能优化
5. **持续**：实战项目、反爬虫对抗

**祝您学习顺利！** 🚀
